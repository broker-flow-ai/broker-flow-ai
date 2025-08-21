from fpdf import FPDF
import os

# Create inbox directory if it doesn't exist
if not os.path.exists("inbox"):
    os.makedirs("inbox")

def create_sample_pdf(filename, title, client_info, details, notes):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    content = [title, ""] + client_info + [""] + details + [""] + notes
    
    for line in content:
        pdf.cell(0, 10, txt=line, ln=True)
    
    pdf.output(filename)

# 1. Flotta Auto - Trasporto Pubblico
create_sample_pdf(
    "inbox/sample_flotta_tp.pdf",
    "Richiesta Preventivo Assicurativo - Flotta Auto",
        content = [
        "Richiesta Preventivo Assicurativo - Flotta Auto",
        "",
        "Cliente: Marco Verdi",
        "Azienda: Verdi Autobus SRL",
        "Settore: Trasporti",
        "Indirizzo: Via Napoli 25, 80135 Napoli (NA)",
        "Telefono: 0811234567",
        "Email: m.verdi@verdiautobus.it"
    ],,
    [
        "Dettaglio Veicoli:",
        "- Targa: NA123NA, Tipo: Autobus, Uso: Trasporto pubblico, Anno: 2019, Valore: 120.000 EUR",
        "- Targa: NA456NA, Tipo: Autobus, Uso: Trasporto pubblico, Anno: 2020, Valore: 130.000 EUR",
        "- Targa: NA789NA, Tipo: Minibus, Uso: Trasporto pubblico, Anno: 2021, Valore: 45.000 EUR"
    ],
    [
        "Note: Richiesta polizza RC Auto per flotta di trasporto pubblico con copertura Kasko."
    ]
)

# 2. RC Professionale - Architetto
create_sample_pdf(
    "inbox/sample_rc_architetto.pdf",
    "Richiesta Preventivo Assicurativo - RC Professionale",
        content = [
        "Richiesta Preventivo Assicurativo - RC Professionale",
        "",
        "Cliente: Ing. Laura Bianchi",
        "Professione: Architetto",
        "Settore: Edilizia",
        "Studio: Corso Italia 15, 10122 Torino (TO)",
        "Telefono: 0119876543",
        "Email: l.bianchi@archstudio.to"
    ],,
    [
        "Dati Attivita':",
        "- Superficie Studio: 120 mq",
        "- Numero dipendenti: 5",
        "- Fatturato annuo: 480.000 EUR",
        "- Attivita': Progettazione architettonica e direzione lavori"
    ],
    [
        "Note: Richiesta polizza RC Professionale con copertura media/max 1.000.000 EUR."
    ]
)

# 3. RC Professionale - Commercialista
create_sample_pdf(
    "inbox/sample_rc_commercialista.pdf",
    "Richiesta Preventivo Assicurativo - RC Professionale",
    [
        "Cliente: Dott. Roberto Ferretti",
        "Professione: Commercialista",
        "Studio: Piazza Garibaldi 8, 50123 Firenze (FI)",
        "Telefono: 0551122334",
        "Email: r.ferretti@studiofi.it"
    ],
    [
        "Dati Attivita':",
        "- Superficie Studio: 90 mq",
        "- Numero dipendenti: 4",
        "- Fatturato annuo: 320.000 EUR",
        "- Attivita': Consulenza fiscale e revisione contabile"
    ],
    [
        "Note: Richiesta polizza RC Professionale con copertura Cyber Risk incluso."
    ]
)

# 4. Flotta Auto - Noleggio con conducente
create_sample_pdf(
    "inbox/sample_flotta_ncc.pdf",
    "Richiesta Preventivo Assicurativo - Flotta Auto",
    [
        "Cliente: Stefano Romano",
        "Azienda: Roma Taxi Service SRL",
        "Indirizzo: Via Appia 500, 00184 Roma (RM)",
        "Telefono: 065556677",
        "Email: info@romataxi.it"
    ],
    [
        "Dettaglio Veicoli:",
        "- Targa: RM100RM, Tipo: Berlina, Uso: NCC, Anno: 2020, Valore: 25.000 EUR",
        "- Targa: RM101RM, Tipo: Berlina, Uso: NCC, Anno: 2021, Valore: 28.000 EUR",
        "- Targa: RM102RM, Tipo: Berlina, Uso: NCC, Anno: 2020, Valore: 25.000 EUR",
        "- Targa: RM103RM, Tipo: Berlina, Uso: NCC, Anno: 2021, Valore: 28.000 EUR"
    ],
    [
        "Note: Richiesta polizza RC Auto per flotta NCC con copertura infortuni passeggeri."
    ]
)

# 5. RC Professionale - Avvocato
create_sample_pdf(
    "inbox/sample_rc_avvocato.pdf",
    "Richiesta Preventivo Assicurativo - RC Professionale",
    [
        "Cliente: Avv. Giulia Martini",
        "Professione: Avvocato",
        "Studio: Via Montenapoleone 12, 20121 Milano (MI)",
        "Telefono: 028889900",
        "Email: g.martini@studiolegalemi.it"
    ],
    [
        "Dati Attivita':",
        "- Superficie Studio: 150 mq",
        "- Numero dipendenti: 8",
        "- Fatturato annuo: 750.000 EUR",
        "- Attivita': Diritto civile e penale"
    ],
    [
        "Note: Richiesta polizza RC Professionale con copertura D&O incluso."
    ]
)

# 6. Flotta Auto - Autotrasporto
create_sample_pdf(
    "inbox/sample_flotta_autotrasporto.pdf",
    "Richiesta Preventivo Assicurativo - Flotta Auto",
    [
        "Cliente: Luca Esposito",
        "Azienda: Esposito Trasporti SRL",
        "Indirizzo: Via Salara 33, 45100 Rovigo (RO)",
        "Telefono: 0425123456",
        "Email: l.esposito@espositotrasporti.it"
    ],
    [
        "Dettaglio Veicoli:",
        "- Targa: RO111RO, Tipo: Tir, Uso: Autotrasporto, Anno: 2018, Valore: 80.000 EUR",
        "- Targa: RO222RO, Tipo: Tir, Uso: Autotrasporto, Anno: 2019, Valore: 85.000 EUR",
        "- Targa: RO333RO, Tipo: Tir, Uso: Autotrasporto, Anno: 2020, Valore: 90.000 EUR"
    ],
    [
        "Note: Richiesta polizza RC Auto per autotrasporto con copertura merci trasportate."
    ]
)

# 7. RC Professionale - Ingegnere
create_sample_pdf(
    "inbox/sample_rc_ingegnere.pdf",
    "Richiesta Preventivo Assicurativo - RC Professionale",
    [
        "Cliente: Ing. Marco De Luca",
        "Professione: Ingegnere Civile",
        "Studio: Via dei Mille 45, 80134 Napoli (NA)",
        "Telefono: 0813334445",
        "Email: m.deluca@ingegneriassociati.na"
    ],
    [
        "Dati Attivita':",
        "- Superficie Studio: 110 mq",
        "- Numero dipendenti: 6",
        "- Fatturato annuo: 520.000 EUR",
        "- Attivita': Progettazione strutturale e direzione lavori"
    ],
    [
        "Note: Richiesta polizza RC Professionale con copertura Pollution Liability incluso."
    ]
)

# 8. Flotta Auto - Concessionaria
create_sample_pdf(
    "inbox/sample_flotta_concessionaria.pdf",
    "Richiesta Preventivo Assicurativo - Flotta Auto",
    [
        "Cliente: Giuseppe Ferrari",
        "Azienda: Ferrari Motori SRL",
        "Indirizzo: Via Emilia 1000, 41124 Modena (MO)",
        "Telefono: 0599876543",
        "Email: g.ferrari@ferrarimotori.it"
    ],
    [
        "Dettaglio Veicoli:",
        "- Targa: MO100MO, Tipo: Auto nuova, Uso: Test drive, Anno: 2022, Valore: 35.000 EUR",
        "- Targa: MO101MO, Tipo: Auto nuova, Uso: Test drive, Anno: 2022, Valore: 40.000 EUR",
        "- Targa: MO102MO, Tipo: Auto usata, Uso: Vendita, Anno: 2019, Valore: 20.000 EUR",
        "- Targa: MO103MO, Tipo: Auto usata, Uso: Vendita, Anno: 2020, Valore: 25.000 EUR"
    ],
    [
        "Note: Richiesta polizza RC Auto per concessionaria con copertura auto showroom."
    ]
)

# 9. RC Professionale - Medico Specialista
create_sample_pdf(
    "inbox/sample_rc_medico_specialista.pdf",
    "Richiesta Preventivo Assicurativo - RC Professionale",
    [
        "Cliente: Dr. Alessandro Ricci",
        "Professione: Medico Specialista - Cardiologia",
        "Studio: Via Veneto 30, 00187 Roma (RM)",
        "Telefono: 0677788899",
        "Email: a.ricci@cardioclinic.rm"
    ],
    [
        "Dati Attivita':",
        "- Superficie Studio: 200 mq",
        "- Numero dipendenti: 12",
        "- Fatturato annuo: 1.200.000 EUR",
        "- Attivita': Visite cardiologiche e interventi ambulatoriali"
    ],
    [
        "Note: Richiesta polizza RC Professionale con copertura infortuni pazienti incluso."
    ]
)

# 10. Flotta Auto - Traslochi
create_sample_pdf(
    "inbox/sample_flotta_traslochi.pdf",
    "Richiesta Preventivo Assicurativo - Flotta Auto",
    [
        "Cliente: Paolo Moretti",
        "Azienda: Moretti Traslochi SRL",
        "Indirizzo: Via Tiburtina 800, 00131 Roma (RM)",
        "Telefono: 0644455566",
        "Email: info@morettitraslochi.it"
    ],
    [
        "Dettaglio Veicoli:",
        "- Targa: RM200RM, Tipo: Furgone, Uso: Traslochi, Anno: 2019, Valore: 22.000 EUR",
        "- Targa: RM201RM, Tipo: Furgone, Uso: Traslochi, Anno: 2020, Valore: 24.000 EUR",
        "- Targa: RM202RM, Tipo: Furgone, Uso: Traslochi, Anno: 2021, Valore: 26.000 EUR"
    ],
    [
        "Note: Richiesta polizza RC Auto per flotta traslochi con copertura danni mobili clienti."
    ]
)

# 11. RC Professionale - Notaio
create_sample_pdf(
    "inbox/sample_rc_notaio.pdf",
    "Richiesta Preventivo Assicurativo - RC Professionale",
    [
        "Cliente: Dott. Marco Colombo",
        "Professione: Notaio",
        "Studio: Piazza Castello 15, 20121 Milano (MI)",
        "Telefono: 0255566777",
        "Email: m.colombo@notaiassociati.mi"
    ],
    [
        "Dati Attivita':",
        "- Superficie Studio: 180 mq",
        "- Numero dipendenti: 10",
        "- Fatturato annuo: 850.000 EUR",
        "- Attivita': Rogiti notarili e consulenza legale"
    ],
    [
        "Note: Richiesta polizza RC Professionale con copertura Cyber Risk e D&O incluso."
    ]
)

# 12. Flotta Auto - Distribuzione
create_sample_pdf(
    "inbox/sample_flotta_distribuzione.pdf",
    "Richiesta Preventivo Assicurativo - Flotta Auto",
    [
        "Cliente: Andrea Conti",
        "Azienda: Conti Distribuzione SRL",
        "Indirizzo: Via Dante 200, 25121 Brescia (BS)",
        "Telefono: 0301234567",
        "Email: a.conti@contidistribuzione.it"
    ],
    [
        "Dettaglio Veicoli:",
        "- Targa: BS300BS, Tipo: Furgone, Uso: Distribuzione, Anno: 2020, Valore: 18.000 EUR",
        "- Targa: BS301BS, Tipo: Furgone, Uso: Distribuzione, Anno: 2021, Valore: 20.000 EUR",
        "- Targa: BS302BS, Tipo: Furgone, Uso: Distribuzione, Anno: 2020, Valore: 18.000 EUR"
    ],
    [
        "Note: Richiesta polizza RC Auto per flotta distribuzione con copertura furto merce."
    ]
)

# 13. RC Professionale - Psicologo
create_sample_pdf(
    "inbox/sample_rc_psicologo.pdf",
    "Richiesta Preventivo Assicurativo - RC Professionale",
    [
        "Cliente: Dott.ssa Elena Rossi",
        "Professione: Psicologo",
        "Studio: Via Manzoni 55, 16121 Genova (GE)",
        "Telefono: 0109998877",
        "Email: e.rossi@psicologogenova.it"
    ],
    [
        "Dati Attivita':",
        "- Superficie Studio: 70 mq",
        "- Numero dipendenti: 2",
        "- Fatturato annuo: 95.000 EUR",
        "- Attivita': Terapia individuale e di coppia"
    ],
    [
        "Note: Richiesta polizza RC Professionale con copertura Privacy e Dati Personali incluso."
    ]
)

# 14. Flotta Auto - Noleggio Lungo Termine
create_sample_pdf(
    "inbox/sample_flotta_noleggio.pdf",
    "Richiesta Preventivo Assicurativo - Flotta Auto",
    [
        "Cliente: Roberto Marchetti",
        "Azienda: Marchetti Rent SRL",
        "Indirizzo: Via Bologna 400, 20100 Milano (MI)",
        "Telefono: 0233344555",
        "Email: r.marchetti@marchettirent.it"
    ],
    [
        "Dettaglio Veicoli:",
        "- Targa: MI400MI, Tipo: Berlina, Uso: Noleggio, Anno: 2021, Valore: 27.000 EUR",
        "- Targa: MI401MI, Tipo: Berlina, Uso: Noleggio, Anno: 2021, Valore: 27.000 EUR",
        "- Targa: MI402MI, Tipo: SUV, Uso: Noleggio, Anno: 2022, Valore: 35.000 EUR",
        "- Targa: MI403MI, Tipo: SUV, Uso: Noleggio, Anno: 2022, Valore: 35.000 EUR"
    ],
    [
        "Note: Richiesta polizza RC Auto per noleggio lungo termine con copertura Kasko completo."
    ]
)

# 15. RC Professionale - Veterinario
create_sample_pdf(
    "inbox/sample_rc_veterinario.pdf",
    "Richiesta Preventivo Assicurativo - RC Professionale",
    [
        "Cliente: Dr. Matteo Fontana",
        "Professione: Veterinario",
        "Clinica: Via Parini 25, 35129 Padova (PD)",
        "Telefono: 0498887766",
        "Email: m.fontana@veterinariopadova.it"
    ],
    [
        "Dati Attivita':",
        "- Superficie Clinica: 150 mq",
        "- Numero dipendenti: 5",
        "- Fatturato annuo: 280.000 EUR",
        "- Attivita': Visite veterinarie e interventi chirurgici"
    ],
    [
        "Note: Richiesta polizza RC Professionale con copertura danni animali incluso."
    ]

)

print("15 additional sample PDF files created in inbox/")