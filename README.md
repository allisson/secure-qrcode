# secure-qrcode
[![Build Status](https://github.com/allisson/secure-qrcode/actions/workflows/lint-and-tests.yml/badge.svg)](https://github.com/allisson/secure-qrcode/actions)
[![Docker Repository on Quay](https://quay.io/repository/allisson/secure-qrcode/status "Docker Repository on Quay")](https://quay.io/repository/allisson/secure-qrcode)

Encrypt your data using the modern ChaCha20-Poly1305 cipher and export it into a secure QR code.

## about the versions

The current version "2.x" is incompatible with version "1.x".

To encrypt and decrypt QR codes using version "1.x" use this documentation: https://github.com/allisson/secure-qrcode/tree/v1.6.0

## how it works

The system receives your key and uses a key derivation function with PBKDF2 to obtain a 32-byte derived key to be applied to the ChaCha20-Poly1305 algorithm.

## access via browser

Open the url https://secure-qrcode.onrender.com on your browser (This is a free instance type and will stop upon inactivity, so be patient).

If you want to run this on your local machine, see the next section.

## run the api

The server can be started using a docker image:

```bash
docker run --rm -p 8000:8000 quay.io/allisson/secure-qrcode
```

Now the API server will be running on port 8000 and you can open the url http://localhost:8000 on your browser.

## api documentation

You can access the API documentation using these two endpoints:
- http://localhost:8000/docs
- http://localhost:8000/redoc

## generate a secure QR code

Call the API passing at least the plaintext and key fields:

```bash
curl --location 'http://localhost:8000/v1/encode' \
--header 'Content-Type: application/json' \
--data '{
    "plaintext": "my super secret text",
    "key": "my super secret key"
}' | jq -r '.content' | base64 --decode > qrcode.png
```

Now you can open the qrcode.png file and do whatever you want.

## decrypt the QR code

Use any program that read a QR code, the content will be something like this:

```json
{
    "salt": "LC1bxUNUpMnt/mae1KDNiA==",
    "iterations": 1200000,
    "associated_data": "0WdPVTKSb/a6KjB3NgjFww==",
    "nonce": "FgmmR8D1Su13HgUO",
    "ciphertext": "4FIQ8LAlztzaToyElulDcPAReKGnOd2TFYiH1P9ZatIOuHN+"
}
```

Now call the API passing the encrypted_data and the key:

```bash
curl --location 'http://localhost:8000/v1/decode' \
--header 'Content-Type: application/json' \
--data '{
    "encrypted_data": {
        "salt": "LC1bxUNUpMnt/mae1KDNiA==",
        "iterations": 1200000,
        "associated_data": "0WdPVTKSb/a6KjB3NgjFww==",
        "nonce": "FgmmR8D1Su13HgUO",
        "ciphertext": "4FIQ8LAlztzaToyElulDcPAReKGnOd2TFYiH1P9ZatIOuHN+"
    },
    "key": "my super secret key"
}' | jq
```

```json
{
  "decrypted_data": "my super secret text"
}
```

## change the value of PBKDF2 iterations

The default value for PBKDF2 iterations is 1200000, you can change this value using the "secure_qrcode_pbkdf2_iterations" environment variable.

```
docker run --rm -p 8000:8000 -e secure_qrcode_pbkdf2_iterations=1000000 quay.io/allisson/secure-qrcode
```
