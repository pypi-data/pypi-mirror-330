import time
from datetime import timedelta

import pytest
from ddeutil.observe.auth.securities import (
    create_access_token,
    create_refresh_token,
    decode_access_token,
    decode_refresh_token,
)
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError


def test_access_token():
    token = create_access_token(
        {"sub": "demo"}, expires_delta=timedelta(seconds=10)
    )
    payload = decode_access_token(token)
    assert payload["sub"] == "demo"


def test_access_token_raise():
    token = create_access_token(
        {"sub": "demo"}, expires_delta=timedelta(seconds=0.1)
    )
    time.sleep(0.2)
    with pytest.raises(ExpiredSignatureError):
        decode_access_token(token)

    with pytest.raises(InvalidSignatureError):
        decode_access_token(token[:-6] + "extend")


def test_refresh_token():
    token = create_refresh_token(
        {"sub": "demo"}, expires_delta=timedelta(seconds=10)
    )
    payload = decode_refresh_token(token)
    assert payload["sub"] == "demo"


def test_refresh_token_raise():
    token = create_refresh_token(
        {"sub": "demo"}, expires_delta=timedelta(seconds=0.1)
    )
    time.sleep(0.2)
    with pytest.raises(ExpiredSignatureError):
        decode_refresh_token(token)

    with pytest.raises(InvalidSignatureError):
        decode_access_token(token[:-6] + "extend")
