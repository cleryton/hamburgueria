import smtplib
from email.message import EmailMessage
from flask import current_app


def enviar_email(destinatario, assunto, corpo, anexo_path=None):
    """Envia um e-mail simples, com anexo opcional (ex.: relatorio em PDF)."""
    config = current_app.config

    if not config.get("SMTP_HOST") or not config.get("SMTP_USER"):
        current_app.logger.warning(
            "SMTP nao configurado (.env) — e-mail nao enviado, apenas simulado."
        )
        return False

    msg = EmailMessage()
    msg["Subject"] = assunto
    msg["From"] = config["SMTP_USER"]
    msg["To"] = destinatario
    msg.set_content(corpo)

    if anexo_path:
        with open(anexo_path, "rb") as f:
            dados = f.read()
        msg.add_attachment(
            dados,
            maintype="application",
            subtype="pdf",
            filename=anexo_path.split("/")[-1],
        )

    with smtplib.SMTP(config["SMTP_HOST"], config["SMTP_PORT"]) as smtp:
        smtp.starttls()
        smtp.login(config["SMTP_USER"], config["SMTP_PASSWORD"])
        smtp.send_message(msg)

    return True


def notificar_estoque_baixo(insumos_criticos):
    if not insumos_criticos:
        return False

    gerente_email = current_app.config.get("GERENTE_EMAIL")
    if not gerente_email:
        return False

    linhas = [
        f"- {i.nome}: {i.quantidade_estoque} {i.unidade_medida} "
        f"(minimo: {i.estoque_minimo} {i.unidade_medida})"
        for i in insumos_criticos
    ]
    corpo = "Os seguintes insumos estao abaixo do estoque minimo:\n\n" + "\n".join(linhas)

    return enviar_email(gerente_email, "Alerta de estoque baixo", corpo)


def enviar_relatorio_diario(caminho_pdf):
    gerente_email = current_app.config.get("GERENTE_EMAIL")
    if not gerente_email:
        return False

    return enviar_email(
        gerente_email,
        "Relatorio diario de vendas",
        "Segue em anexo o relatorio de vendas do dia.",
        anexo_path=caminho_pdf,
    )
