def generate_email(client_name, policy_paths):
    subject = "Il tuo preventivo assicurativo"
    body = f"""
    Gentile {client_name},

    in allegato trova i preventivi richiesti.

    Per qualsiasi dubbio, siamo a disposizione.

    Cordiali saluti,
    BrokerFlow AI
    """

    # TODO: Add attachments and send via SMTP or Gmail API

    return subject, body