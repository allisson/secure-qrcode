import pytest
from fastapi.testclient import TestClient

from secure_qrcode.api import app
from secure_qrcode.models import EncryptedData


@pytest.fixture
def key():
    return "my super secret key"


@pytest.fixture
def plaintext():
    return "super secret text"


@pytest.fixture
def sample_encrypted_data():
    """Sample encrypted data for testing decrypt operations."""
    return EncryptedData(
        salt="KtiCW1E0VLupOXOtpDIlZQ==",
        iterations=1200000,
        associated_data="JFPRP6/RMmCIn3DLjA/ceg==",
        nonce="LbF9P5FwPYyGCTJM",
        ciphertext="/N8WF0+QnqsDhOQ9iWuhWrXgbrZlG4Hqm9cYt/QO9Msu",
    )


@pytest.fixture
def client():
    return TestClient(app)
