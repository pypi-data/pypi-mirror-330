import os


class AuthConfig:
    enforce_token_validation: bool
    auth_authority_url: str
    trusted_issuer: str
    allowed_audiences: list[str]

    def __init__(self):
        self.auth_authority_url = os.getenv("AUTH_AUTHORITY_URL")
        self.allowed_audiences = os.getenv("VALID_AUDIENCES", "").split(",")
        self.trusted_issuer = os.getenv("TRUSTED_ISSUER")
        self.enforce_token_validation = bool(os.getenv("VALIDATE_TOKEN", None))
