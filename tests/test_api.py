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
        nonce="c2nduzQLo4sWOe3n",
        header="oheZpcpquDA7CoUuAi8Mng==",
        ciphertext="7WXqkkf4CWlH5A2vmXDbyMc=",
        tag="l027RcLlp2acAUxIxfYiAg==",
    )
    request = DecodeRequest(encrypted_data=encrypted_data, key=key)
    response = client.post("/v1/decode", json=request.model_dump())

    assert response.status_code == 201
    response_data = response.json()
    assert response_data["decrypted_data"] == plaintext


def test_decode_error(client, plaintext, key):
    encrypted_data = EncryptedData(
        nonce="c2nduzQLo4sWOe3n",
        header="oheZpcpquDA7CoUuAi8Mng==",
        ciphertext="7WXqkkf4CWlH5A2vmXDbyMc=",
        tag="l027RcLlp2acAUxIxfYiAg==",
    )
    encrypted_data.header = b64encode(b"invalid-header").decode("utf-8")
    request = DecodeRequest(encrypted_data=encrypted_data, key=key)
    response = client.post("/v1/decode", json=request.model_dump())

    assert response.status_code == 400
    response_data = response.json()
    assert response_data["message"] == "Incorrect decryption, please check your data"


def test_healthz(client):
    response = client.get("/healthz")

    assert response.status_code == 200
