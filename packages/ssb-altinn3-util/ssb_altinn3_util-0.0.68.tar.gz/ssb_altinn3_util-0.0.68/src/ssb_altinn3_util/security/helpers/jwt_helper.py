import base64
import json
from typing import Dict

from jwt import PyJWKClient
import jwt

from fastapi import HTTPException
from ssb_altinn3_util.security.auth_config import AuthConfig

config = AuthConfig()

client = PyJWKClient(uri=f"{config.auth_authority_url}/protocol/openid-connect/certs")


def validate_token(token: str, config: AuthConfig) -> str:
    try:
        signing_key = client.get_signing_key_from_jwt(token=token)

        token_data = jwt.decode(
            jwt=token,
            key=signing_key.key,
            algorithms=["RS256"],
            audience=config.allowed_audiences,
            issuer=config.trusted_issuer,
            options={"verify_exp": True},
        )
        return _get_email_from_json(token_payload_json=token_data)
    except Exception as e:
        raise HTTPException(
            status_code=401, detail=f"Failed to authenticate user with error: {e}"
        )


def get_user_email_from_token(token: str) -> str:
    """Get the user email from the jwt token"""
    token = token.split(sep=".")[1]
    token_decoded = base64.b64decode(token + "==").decode("UTF-8")
    token_json: Dict = json.loads(token_decoded)

    return _get_email_from_json(token_payload_json=token_json)


def _get_email_from_json(token_payload_json: dict) -> str:
    email: str = token_payload_json.get("email")

    if not email:
        preferred_username: str = token_payload_json.get("preferred_username")

        if not preferred_username:
            return ""

        email = (
            preferred_username
            if preferred_username.endswith("@ssb.no")
            else f"{preferred_username}@ssb.no"
        )

    return email
