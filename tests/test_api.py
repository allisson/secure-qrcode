from base64 import b64encode

from secure_qrcode.models import DecodeRequest, EncodeRequest


def test_index(client):
    """Test the home page endpoint."""
    response = client.get("/")

    assert response.status_code == 200


def test_encode(client, plaintext, key):
    """Test encoding plaintext to QR code."""
    request = EncodeRequest(plaintext=plaintext, key=key)
    response = client.post("/v1/encode", json=request.model_dump())

    assert response.status_code == 201
    response_data = response.json()
    assert response_data["content"]
    assert response_data["media_type"] == "image/png"


def test_decode(client, plaintext, key, sample_encrypted_data):
    """Test decoding QR code to plaintext."""
    request = DecodeRequest(encrypted_data=sample_encrypted_data, key=key)
    response = client.post("/v1/decode", json=request.model_dump())

    assert response.status_code == 201
    response_data = response.json()
    assert response_data["decrypted_data"] == plaintext


def test_decode_error(client, key, sample_encrypted_data):
    """Test decoding with invalid data returns error."""
    encrypted_data = sample_encrypted_data.model_copy(
        update={"associated_data": b64encode(b"invalid-aad").decode()}
    )
    request = DecodeRequest(encrypted_data=encrypted_data, key=key)
    response = client.post("/v1/decode", json=request.model_dump())

    assert response.status_code == 400
    response_data = response.json()
    assert response_data["message"] == "Incorrect decryption, please check your data"


def test_healthz(client):
    """Test the health check endpoint."""
    response = client.get("/healthz")

    assert response.status_code == 200
