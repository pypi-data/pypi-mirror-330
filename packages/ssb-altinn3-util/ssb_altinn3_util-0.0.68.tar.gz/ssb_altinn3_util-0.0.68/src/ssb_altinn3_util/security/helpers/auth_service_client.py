import json
import os
import requests
from fastapi import status

from ssb_altinn3_util.security.authorization_request import AuthorizationRequest
from ssb_altinn3_util.security.authorization_result import AuthorizationResult

AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL")


def verify_access(user_email: str, requested_role: str) -> AuthorizationResult:
    auth_request = AuthorizationRequest(
        user_email=user_email, requested_role=requested_role
    )
    url = f"{AUTH_SERVICE_URL}/auth/authorize"
    response = requests.post(url=url, data=auth_request.json())
    if response.status_code != 200:
        # If any error from auth-service, create "empty" result object containing the error
        return AuthorizationResult(
            access_granted=False,
            status_code=response.status_code,
            error_message=response.content.decode("UTF-8"),
            allowed_forms_read=[],
            allowed_forms_write=[],
        )

    decoded = response.content.decode("UTF-8")
    return AuthorizationResult(**json.loads(decoded))
