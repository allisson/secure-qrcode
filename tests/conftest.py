import pytest
from fastapi.testclient import TestClient

from secure_qrcode.api import app


@pytest.fixture
def key():
    return "my super secret key"


@pytest.fixture
def plaintext():
    return "super secret text"


@pytest.fixture
def client():
    return TestClient(app)
