# secure-qrcode
[![Build Status](https://github.com/allisson/secure-qrcode/workflows/build/badge.svg)](https://github.com/allisson/secure-qrcode/actions)
[![Docker Repository on Quay](https://quay.io/repository/allisson/secure-qrcode/status "Docker Repository on Quay")](https://quay.io/repository/allisson/secure-qrcode)

Encrypt your data using the modern ChaCha20-Poly1305 cipher and export it into a secure QR code.

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
    "nonce": "PAhk6TKJAT7taGOH",
    "header": "/wxYPzrrSRLUTQ3WjpmpMA==",
    "ciphertext": "QygEEzUS2wFUmTJtupBtLHrf92Y=",
    "tag": "wNIaFK4YdTRa4p3PbvJboA=="
}
```

Now call the API passing the encrypted_data and the key:

```bash
curl --location 'http://localhost:8000/v1/decode' \
--header 'Content-Type: application/json' \
--data '{
    "encrypted_data": {
        "nonce": "PAhk6TKJAT7taGOH",
        "header": "/wxYPzrrSRLUTQ3WjpmpMA==",
        "ciphertext": "QygEEzUS2wFUmTJtupBtLHrf92Y=",
        "tag": "wNIaFK4YdTRa4p3PbvJboA=="
    },
    "key": "my super secret key"
}' | jq
```

```json
{
  "decrypted_data": "my super secret text"
}
```

## about left padding char

The ChaCha20-Poly1305 works with a 32-byte secret key. When you use a secret key with less than 32 bytes, we need to use left padding until the required size is reached.

The default character for the left padding is the white space, which can be changed using the `"secure_qrcode_left_padding_char"` environment variable.

For example, when using the secret key `"my super secret key"` the value used in the encryption function will be `"my super secret key             "`.

To start the server using another left padding char:

```bash
docker run --rm -p 8000:8000 -e secure_qrcode_left_padding_char=9 quay.io/allisson/secure-qrcode
```
