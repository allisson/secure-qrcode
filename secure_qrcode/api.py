from base64 import b64encode

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from secure_qrcode.config import settings
from secure_qrcode.crypto import decrypt, encrypt
from secure_qrcode.exceptions import DecryptError
from secure_qrcode.models import (
    DecodeRequest,
    DecodeResponse,
    DecryptErrorResponse,
    EncodeRequest,
    EncodeResponse,
)
from secure_qrcode.qrcode import make

app = FastAPI(
    title="Secure QR code",
    description="Encrypt your data using the modern ChaCha20-Poly1305 cipher and export it into a secure QR code",
)


@app.exception_handler(DecryptError)
def decrypt_error_exception_handler(request: Request, exc: DecryptError):
    return JSONResponse(
        status_code=400,
        content={"message": "Incorrect decryption, please check your data"},
    )


@app.post("/v1/encode", status_code=201)
def encode(request: EncodeRequest) -> EncodeResponse:
    encrypted_data = encrypt(request.plaintext, request.key, settings.left_padding_char)
    img_io = make(
        encrypted_data,
        error_correction=request.error_correction,
        box_size=request.box_size,
        border=request.border,
    )
    return EncodeResponse(content=b64encode(img_io.getvalue()).decode("utf-8"), media_type="image/png")


@app.post(
    "/v1/decode",
    status_code=201,
    responses={400: {"model": DecryptErrorResponse, "description": "Incorrect decryption"}},
)
def decode(request: DecodeRequest) -> DecodeResponse:
    decrypted_data = decrypt(request.encrypted_data, request.key, settings.left_padding_char)
    return DecodeResponse(decrypted_data=decrypted_data)
