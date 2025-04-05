from base64 import b64encode

from secure_qrcode.models import DecodeRequest, EncodeRequest, EncryptedData


def test_index(client):
    response = client.get("/")

    assert response.status_code == 200


def test_encode(client, plaintext, key):
    request = EncodeRequest(plaintext=plaintext, key=key)
    response = client.post("/v1/encode", json=request.model_dump())

    assert response.status_code == 201
    response_data = response.json()
    assert response_data["content"]
    assert response_data["media_type"] == "image/png"


def test_decode(client, plaintext, key):
    encrypted_data = EncryptedData(
        salt="KtiCW1E0VLupOXOtpDIlZQ==",
        iterations=1200000,
        associated_data="JFPRP6/RMmCIn3DLjA/ceg==",
        nonce="LbF9P5FwPYyGCTJM",
        ciphertext="/N8WF0+QnqsDhOQ9iWuhWrXgbrZlG4Hqm9cYt/QO9Msu",
    )
    request = DecodeRequest(encrypted_data=encrypted_data, key=key)
    response = client.post("/v1/decode", json=request.model_dump())

    assert response.status_code == 201
    response_data = response.json()
    assert response_data["decrypted_data"] == plaintext


def test_decode_error(client, key):
    encrypted_data = EncryptedData(
        salt="KtiCW1E0VLupOXOtpDIlZQ==",
        iterations=1200000,
        associated_data="JFPRP6/RMmCIn3DLjA/ceg==",
        nonce="LbF9P5FwPYyGCTJM",
        ciphertext="/N8WF0+QnqsDhOQ9iWuhWrXgbrZlG4Hqm9cYt/QO9Msu",
    )
    encrypted_data.associated_data = b64encode(b"invalid-aad").decode("utf-8")
    request = DecodeRequest(encrypted_data=encrypted_data, key=key)
    response = client.post("/v1/decode", json=request.model_dump())

    assert response.status_code == 400
    response_data = response.json()
    assert response_data["message"] == "Incorrect decryption, please check your data"


def test_healthz(client):
    response = client.get("/healthz")

    assert response.status_code == 200
