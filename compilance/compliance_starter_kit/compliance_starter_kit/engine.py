import os, csv, json, datetime, hashlib
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, ElementTree, tostring

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
RULES = BASE / "rules.yaml"
XSD = BASE / "schema.xsd"
OUT = BASE / "out"
OUT.mkdir(exist_ok=True)

def _read_csv(path):
    def parse_num(v):
        try:
            return float(v)
        except Exception:
            return v
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        rd = csv.DictReader(f)
        for r in rd:
            rows.append({k: parse_num(v) for k, v in r.items()})
    return rows

def load_rules():
    # naive YAML parser for this simple structure
    text = RULES.read_text(encoding="utf-8")
    # extremely simplified: split by '- id:' blocks
    rules = []
    version = "NA"
    for line in text.splitlines():
        if line.startswith("version:"):
            version = line.split(":",1)[1].strip()
    blocks = text.split("\n  - id: ")
    for b in blocks[1:]:
        lines = b.splitlines()
        rid = lines[0].strip()
        d = {"id": rid}
        for ln in lines[1:]:
            if not ln.strip(): 
                continue
            key, val = ln.strip().split(":",1)
            d[key.strip()] = val.strip()
        rules.append(d)
    return version, rules

def eval_rule(rule, row, table, context):
    env = {"abs": abs, "all": all, "isinstance": isinstance}
    env.update(row)
    env["table"] = table
    env["context"] = context
    env["numeric_values"] = [v for v in row.values() if isinstance(v,(int,float))]
    env["date_values"] = [row.get(k) for k in row if "data" in k or k in ("decorrenza","scadenza")]
    try:
        if "transform" in rule:
            # e.g., "ramo_normativo = {...}.get(ramo, '99')"
            exec(rule["transform"], {}, env)
            # copy back any new keys
            for k,v in env.items():
                if k not in row and k.endswith("_normativo"):
                    row[k] = v
            return ("TRANSFORM", None)
        expr = rule.get("assert")
        if expr:
            ok = eval(expr, {}, env)
            if not ok:
                return ("FAIL", rule.get("message",""))
            else:
                return ("PASS", None)
        return ("PASS", None)
    except Exception as e:
        return ("ERROR", str(e))

def hash_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def main(periodo="2025-Q3"):
    policy = _read_csv(DATA / "policy.csv")
    sinistro = _read_csv(DATA / "sinistro.csv")
    transazione = _read_csv(DATA / "transazione.csv")
    intermediario = _read_csv(DATA / "intermediario.csv")
    cliente = _read_csv(DATA / "anagrafica_cliente.csv")

    version, rules = load_rules()
    context = {"policy_ids": set(p["id"] for p in policy)}

    violations = []
    blocking = 0

    def apply(table_name, rows):
        nonlocal blocking
        for r in rows:
            for rule in rules:
                cond = rule.get("when","")
                # crude filter
                if table_name not in cond:  # quick check
                    if "table in" in cond and table_name in cond:
                        pass
                    else:
                        continue
                status, msg = eval_rule(rule, r, table_name, context)
                if status in ("FAIL","ERROR"):
                    violations.append({
                        "rule": rule["id"],
                        "table": table_name,
                        "row_id": r.get("id") or r.get("policy_id"),
                        "severity": rule.get("severity","WARN"),
                        "message": msg
                    })
                    if rule.get("severity","WARN") == "BLOCKING":
                        blocking += 1

    apply("policy", policy)
    apply("sinistro", sinistro)
    apply("transazione", transazione)

    if blocking > 0:
        out_viols = OUT / "violations.json"
        out_viols.write_text(json.dumps(violations, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"BLOCKING ERRORS: {blocking}. See {out_viols}")
        return

    # Aggregates
    premi = sum(p.get("premio_netto",0) for p in policy if isinstance(p.get("premio_netto",0),(int,float)))
    pagati = sum(s.get("pagato",0) for s in sinistro if isinstance(s.get("pagato",0),(int,float)))
    riserva_finale = sum(s.get("riserva",0) for s in sinistro if isinstance(s.get("riserva",0),(int,float)))

    # XML build
    root = Element("SegnalazionePeriodica")
    SubElement(root, "Periodo").text = periodo
    inter = SubElement(root, "Intermediario")
    SubElement(inter, "Codice").text = str(intermediario[0]["codice"])
    SubElement(inter, "Denominazione").text = str(intermediario[0]["denominazione"])
    agg = SubElement(root, "Aggregati")
    SubElement(agg, "Premi").text = f"{premi:.2f}"
    SubElement(agg, "SinistriPagati").text = f"{pagati:.2f}"
    SubElement(agg, "RiservaFinale").text = f"{riserva_finale:.2f}"

    xml_path = OUT / "report.xml"
    ElementTree(root).write(xml_path, encoding="utf-8", xml_declaration=True)

    # Evidence pack (hashes)
    evidence = OUT / "evidence.txt"
    with open(evidence, "w", encoding="utf-8") as ef:
        for p in [DATA / "policy.csv", DATA / "sinistro.csv", DATA / "transazione.csv"]:
            ef.write(f"{p.name}: {hash_file(p)}\n")
        ef.write(f"report.xml: {hash_file(xml_path)}\n")
        ef.write(f"rules.yaml: {hash_file(RULES)}\n")
        ef.write(f"schema.xsd: {hash_file(XSD)}\n")

    # Optional: try XSD validation via lxml if available
    try:
        from lxml import etree
        schema = etree.XMLSchema(etree.parse(str(XSD)))
        doc = etree.parse(str(xml_path))
        schema.assertValid(doc)
        (OUT / "xsd_validation_ok.txt").write_text("VALID", encoding="utf-8")
        print("Report generated and XSD-validated:", xml_path)
    except Exception as e:
        print("Report generated (XSD validation skipped or failed):", xml_path, "|", e)

if __name__ == "__main__":
    main()