import os

import pytest
from fastapi import Request, HTTPException
from pytest_mock.plugin import MockerFixture

import ssb_altinn3_util.security.authenticator_constants as constants
from ssb_altinn3_util.security.form_access import FormAccessValidator
from ssb_altinn3_util.security.role_authorization import authorize


def test_form_validate_ok_1(
    mocker: MockerFixture, fake_auth_result_ok, create_fake_request
):
    result = fake_auth_result_ok()
    mocker.patch.dict(os.environ, {"AUTH_SERVICE_URL": "https://auth.mock"}, clear=True)

    mocker.patch(
        "ssb_altinn3_util.security.helpers.auth_service_client.verify_access",
        return_value=result,
    )

    auth_req: Request = create_fake_request('{"email":"user@email.com"}')

    @authorize(require_role=constants.ROLE_ADMIN)
    def test_me(request: Request):
        validator = FormAccessValidator(request)

        assert validator.verify_form_read_access("RA1234")
        assert validator.verify_form_read_access("RA9999")
        with pytest.raises(HTTPException) as he:
            validator.verify_form_read_access("RA1000")
        assert he.value.status_code == 403
        assert he.value.detail == "User has insufficient access to form 'RA1000'"

    test_me(auth_req)


def test_form_validate_ok_2(
    mocker: MockerFixture, fake_auth_result_ok, create_fake_request
):
    result = fake_auth_result_ok(include_read_all=True)
    mocker.patch.dict(os.environ, {"AUTH_SERVICE_URL": "https://auth.mock"}, clear=True)

    mocker.patch(
        "ssb_altinn3_util.security.helpers.auth_service_client.verify_access",
        return_value=result,
    )

    auth_req: Request = create_fake_request(body='{"email":"user@email.com"}')

    @authorize(require_role=constants.ROLE_ADMIN)
    def test_me(request: Request):
        validator = FormAccessValidator(request)

        assert validator.verify_form_read_access("RA1234")
        assert validator.verify_form_read_access("RA9999")
        assert validator.verify_form_read_access("RA1000")

        with pytest.raises(HTTPException):
            assert not validator.verify_form_write_access("RA1234")
        with pytest.raises(HTTPException):
            assert not validator.verify_form_write_access("RA9999")
        with pytest.raises(HTTPException):
            assert not validator.verify_form_write_access("RA1000")

    test_me(auth_req)
