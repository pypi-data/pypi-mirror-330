import pytest
import base64

from fastapi import Request

from ssb_altinn3_util.security.authorization_result import AuthorizationResult
import ssb_altinn3_util.security.authenticator_constants as constants


@pytest.fixture(scope="function")
def fake_auth_result_ok():
    def create(include_read_all: bool = False, include_write_all: bool = False):
        read_forms = ["RA1234", "RA9999"]
        write_forms = []
        if include_read_all:
            read_forms = [constants.FORM_ACCESS_ALL]
        if include_write_all:
            write_forms = [constants.FORM_ACCESS_ALL]
        return AuthorizationResult(
            access_granted=True,
            status_code=200,
            allowed_forms_read=read_forms,
            allowed_forms_write=write_forms,
        )

    return create


@pytest.fixture(scope="function")
def fake_auth_result_reject():
    return AuthorizationResult(
        access_granted=False,
        status_code=403,
        error_message="Role requirement not satisfied",
        allowed_forms_read=[],
        allowed_forms_write=[],
    )


@pytest.fixture(scope="function")
def create_fake_request():
    def factory(body: str) -> Request:
        encoded = base64.b64encode(bytes(body.encode("UTF-8"))).decode("UTF-8")

        auth_req: Request = Request(
            scope={
                "type": "http",
                "headers": [
                    (
                        "authorization".encode(),
                        f"Bearer eyAiaGVpIjoiaG9wcCJ9.{encoded}.eyAic2lnIjoic2FnIn0=".encode(),
                    )
                ],
            }
        )

        return auth_req

    return factory
