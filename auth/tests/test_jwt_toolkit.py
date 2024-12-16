import jwt
import pytest

from datetime import timedelta
from jwt_utils import JwtConfig, JwtToolkit


@pytest.fixture()
def jwt_config():
    return JwtConfig("test_secret")


@pytest.fixture()
def jwt_toolkit(jwt_config):
    return JwtToolkit(jwt_config)


def test_sign_token_without_payload(jwt_toolkit, jwt_config):
    without_payload = jwt_toolkit._sign_token("test", "test_subject")
    decoded = jwt.decode(without_payload, jwt_config.secret, jwt_config.algorithm)

    assert decoded["sub"] == "test_subject"
    assert decoded["type"] == "test"


def test_sign_token_with_payload(jwt_toolkit, jwt_config):
    with_payload = jwt_toolkit._sign_token("test", "test_subject", {"test": "_test_"}, )
    decoded = jwt.decode(with_payload, jwt_config.secret, jwt_config.algorithm)

    assert decoded["sub"] == "test_subject"
    assert decoded["type"] == "test"
    assert decoded["test"] == "_test_"

    assert decoded.get("exp", None) is None


def test_sign_token_ttl(jwt_toolkit, jwt_config):

    ttl = timedelta(seconds=360)
    token = jwt_toolkit._sign_token("test", "test_subject", {}, ttl)
    decoded = jwt.decode(token, jwt_config.secret, jwt_config.algorithm)

    assert decoded["sub"] == "test_subject"
    assert decoded["type"] == "test"
    assert decoded.get("exp", None) is not None


def test_create_refresh_token(jwt_toolkit):
    refresh_token = jwt_toolkit._create_refresh_token("refresh")
    decoded = jwt.decode(refresh_token, options={"verify_signature": False})

    assert decoded["sub"] == "refresh"
    assert decoded["type"] == "refresh"


def test_create_access_token(jwt_toolkit):
    access_token = jwt_toolkit._create_access_token("access")
    decoded = jwt.decode(access_token, options={"verify_signature": False})

    assert decoded["sub"] == "access"
    assert decoded["type"] == "access"


def test_issue_token(jwt_toolkit):
    access_token, refresh_token = jwt_toolkit.issue_token("test")

    decoded_access = jwt.decode(access_token, options={"verify_signature": False})
    decoded_refresh = jwt.decode(refresh_token, options={"verify_signature": False})

    assert decoded_access["type"] == "access"
    assert decoded_access["sub"] == "test"

    assert decoded_refresh["type"] == "refresh"
    assert decoded_refresh["sub"] == "test"
