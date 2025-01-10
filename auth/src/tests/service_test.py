# must up container before testing
import jwt

import random
import string

import httpx
import pytest

from fastapi import status


AUTH_URL = "http://localhost:8001/api/v1/oauth2"

TEST_USER_USERNAME = "test"
TEST_USER_UID = "0173ddda-44b9-486f-97f2-c1779553112b"


@pytest.fixture(scope="session")
def fetch_access_token():
    token_url = AUTH_URL + "/sign_in"

    data = {"username": "test", "password": "test"}
    response = httpx.post(token_url, json=data)

    json = response.json()
    return json["access_token"], json["refresh_token"]


def test_sign_in():
    token_url = AUTH_URL + "/sign_in"
    data = {"username": "test", "password": "test"}
    response = httpx.post(token_url, json=data)

    json = response.json()

    decoded_access_token = jwt.decode(json["access_token"], options={"verify_signature": False})
    print(decoded_access_token)


def test_fetch_token(fetch_access_token):
    access_token, refresh_token = fetch_access_token

    assert len(access_token.split(".")) == 3
    assert len(refresh_token.split(".")) == 3


def test_verify_valid_token(fetch_access_token):
    access_token, _ = fetch_access_token

    verify_token_url = AUTH_URL + "/verify_token"
    response = httpx.post(verify_token_url, headers={"Authorization": f"Bearer {access_token}"})

    json = response.json()
    decoded = jwt.decode(json.replace("Bearer ", ""), options={"verify_signature": False})

    assert decoded["sub"] == TEST_USER_UID
    assert decoded["username"] == TEST_USER_USERNAME


def test_verify_invalid_token():
    verify_token_url = AUTH_URL + "/verify_token"
    response = httpx.post(verify_token_url, headers={"Authorization": "Bearer invalidtoken"})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_sign_up():
    """
        Gen a random user and sends a sign up request.
        I consider status code == 200 to be success, as well as the return of jwt.
        The problem with this method is that the database stores the values ​​of test users.
    """

    def generate_():
        s = "".join(random.choices(string.ascii_letters + string.digits, k=15))
        return s[:7], s[7:]

    sign_up_url = AUTH_URL + "/sign_up"

    username, password = generate_()
    data = {"username": username, "password": password}

    response = httpx.post(sign_up_url, json=data)

    json = response.json()
    access_token, refresh_token = json["access_token"], json["refresh_token"]

    assert response.status_code == status.HTTP_200_OK
    assert len(access_token.split(".")) == 3
    assert len(refresh_token.split(".")) == 3


def test_verify_refresh_token(fetch_access_token):
    """
        IF token type == refresh_type then an error should occur.
    """

    _, refresh_token = fetch_access_token

    verify_token_url = AUTH_URL + "/verify_token"
    response = httpx.post(verify_token_url, headers={"Authorization": f"Bearer {refresh_token}"})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
