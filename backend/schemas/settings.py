from pydantic import BaseModel


class SmtpSettingsRequest(BaseModel):
    smtp_host: str | None = None
    smtp_port: str | None = None
    smtp_username: str | None = None
    smtp_password: str | None = None
    smtp_sender: str | None = None
    smtp_use_tls: str | None = None


class TestEmailRequest(BaseModel):
    recipient: str
