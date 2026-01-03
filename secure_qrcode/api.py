from base64 import b64encode

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from secure_qrcode.crypto import decrypt, encrypt
from secure_qrcode.exceptions import DecryptError
from secure_qrcode.models import (
    DecodeRequest,
    DecodeResponse,
    DecryptErrorResponse,
    EncodeRequest,
    EncodeResponse,
    HealthResponse,
)
from secure_qrcode.qrcode import make

app = FastAPI(
    title="Secure QR Code",
    description="Encrypt your data using the modern ChaCha20-Poly1305 cipher and export it into a secure QR code",
)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
templates.env.globals["url_for"] = app.url_path_for


@app.exception_handler(DecryptError)
def decrypt_error_exception_handler(request: Request, exc: DecryptError):
    """Handle DecryptError exceptions by returning a JSON error response."""
    return JSONResponse(
        status_code=400,
        content={"message": "Incorrect decryption, please check your data"},
    )


@app.get("/", response_class=HTMLResponse, tags=["home"])
def index(request: Request):
    """Render the home page template."""
    return templates.TemplateResponse(request, "index.html")


@app.post("/v1/encode", status_code=201, tags=["api"])
def encode(request: EncodeRequest) -> EncodeResponse:
    """Encrypt plaintext data and generate a QR code image."""
    encrypted_data = encrypt(request.plaintext, request.key)
    img_io = make(
        encrypted_data,
        error_correction=request.error_correction,
        box_size=request.box_size,
        border=request.border,
    )
    return EncodeResponse(content=b64encode(img_io.getvalue()).decode(), media_type="image/png")


@app.post(
    "/v1/decode",
    status_code=201,
    responses={400: {"model": DecryptErrorResponse, "description": "Incorrect decryption"}},
    tags=["api"],
)
def decode(request: DecodeRequest) -> DecodeResponse:
    """Decrypt encrypted data from a QR code."""
    decrypted_data = decrypt(request.encrypted_data, request.key)
    return DecodeResponse(decrypted_data=decrypted_data)


@app.get("/healthz", tags=["healthcheck"])
def healthz() -> HealthResponse:
    """Health check endpoint to verify service availability."""
    return HealthResponse(success=True)
