from typing import Dict
import base64
import json
import pytest

from ssb_altinn3_util.security.helpers import jwt_helper


@pytest.fixture(scope="function")
def fake_token():
    def create(claims: Dict[str, str]) -> str:
        payload: str = json.dumps(claims)
        return f"Bearer abcd.{base64.b64encode(payload.encode('UTF-8')).decode('UTF-8')}.dcba"

    return create


def test_email_present_ok(fake_token):
    token = fake_token({"email": "test@ssb.no"})

    email = jwt_helper.get_user_email_from_token(token)

    assert email == "test@ssb.no"


def test_no_email_preferred_user_ok1(fake_token):
    token = fake_token({"snailmail": "test@ssb.no", "preferred_username": "bob"})

    email = jwt_helper.get_user_email_from_token(token)

    assert email == "bob@ssb.no"


def test_no_email_preferred_user_ok2(fake_token):
    token = fake_token({"snailmail": "test@ssb.no", "preferred_username": "bob@ssb.no"})

    email = jwt_helper.get_user_email_from_token(token)

    assert email == "bob@ssb.no"


def test_no_identifiers_empty_response(fake_token):
    token = fake_token({"snailmail": "test@ssb.no", "another_username": "bob@ssb.no"})

    email = jwt_helper.get_user_email_from_token(token)

    assert not email
