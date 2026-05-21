import smtplib
from email.message import EmailMessage

from src.configs.configs import settings


def send_password_reset_email(email_to: str, reset_url: str) -> None:
    if not settings.SMTP_ENABLED:
        return

    message = EmailMessage()
    message["Subject"] = "Recuperacao de senha"
    message["From"] = f"{settings.SMTP_FROM_NAME} <{settings.SMTP_FROM_EMAIL}>"
    message["To"] = email_to
    message.set_content(
        "Voce solicitou a recuperacao de senha.\n\n"
        f"Acesse o link para redefinir sua senha:\n{reset_url}\n"
    )

    smtp_class = smtplib.SMTP_SSL if settings.SMTP_USE_SSL else smtplib.SMTP
    with smtp_class(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        if settings.SMTP_USE_TLS and not settings.SMTP_USE_SSL:
            server.starttls()
        if settings.SMTP_USERNAME and settings.SMTP_PASSWORD:
            server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
        server.send_message(message)
