# 🔐 Secure QR Code Generator

[![Build Status](https://github.com/allisson/secure-qrcode/actions/workflows/lint-and-tests.yml/badge.svg)](https://github.com/allisson/secure-qrcode/actions)
[![Docker Image Version](https://img.shields.io/docker/v/allisson/secure-qrcode)](https://hub.docker.com/r/allisson/secure-qrcode)

> 🚀 **Encrypt your sensitive data using modern cryptography and turn it into secure QR codes!**

Transform your private information into unreadable encrypted data using the powerful **ChaCha20-Poly1305** cipher, then encode it as a QR code for easy sharing and storage. 🔒📱

## ✨ Features

- 🔐 **Military-grade encryption** with ChaCha20-Poly1305
- 🏗️ **PBKDF2 key derivation** for enhanced security
- 📱 **QR code generation** for easy data transfer
- 🌐 **RESTful API** with interactive documentation
- 🐳 **Docker support** for easy deployment
- ⚡ **FastAPI backend** for high performance

## 📋 Version Compatibility

⚠️ **Important**: Version "2.x" is **not compatible** with version "1.x".

For legacy "1.x" QR codes, check the [v1.6.0 documentation](https://github.com/allisson/secure-qrcode/tree/v1.6.0). 📚

## 🔍 How It Works

1. 📝 **Input**: Your secret message and encryption key
2. 🔑 **Derivation**: PBKDF2 transforms your key into a 32-byte cryptographic key
3. 🔒 **Encryption**: ChaCha20-Poly1305 encrypts your data with authenticated encryption
4. 📱 **QR Generation**: Encrypted data becomes a scannable QR code

```
Plaintext + Key → PBKDF2 → ChaCha20-Poly1305 → QR Code
```

## 🚀 Quick Start

### 🌐 Try It Online

Visit the [live demo](https://secure-qrcode.onrender.com) in your browser! 🌍

> 💡 **Note**: This is a free instance that may sleep during inactivity. Please be patient! ⏳

### 🐳 Run Locally with Docker

```bash
# Pull and run the API server
docker run --rm -p 8000:8000 allisson/secure-qrcode

# Access the web interface
open http://localhost:8000
```

That's it! Your secure QR code generator is now running locally. 🎉

## 📖 API Documentation

Explore the interactive API docs:
- 📋 **Swagger UI**: http://localhost:8000/docs
- 📄 **ReDoc**: http://localhost:8000/redoc

## 💻 Usage Examples

### 🔐 Generate a Secure QR Code

```bash
curl --location 'http://localhost:8000/v1/encode' \
--header 'Content-Type: application/json' \
--data '{
    "plaintext": "my super secret text",
    "key": "my super secret key"
}' | jq -r '.content' | base64 --decode > secure_qrcode.png

# Your encrypted QR code is saved as secure_qrcode.png! 🖼️
```

### 🔓 Decrypt a QR Code

First, scan your QR code to get the encrypted data (it looks like this):

```json
{
    "salt": "LC1bxUNUpMnt/mae1KDNiA==",
    "iterations": 1200000,
    "associated_data": "0WdPVTKSb/a6KjB3NgjFww==",
    "nonce": "FgmmR8D1Su13HgUO",
    "ciphertext": "4FIQ8LAlztzaToyElulDcPAReKGnOd2TFYiH1P9ZatIOuHN+"
}
```

Then decrypt it:

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

**Response:**
```json
{
  "decrypted_data": "my super secret text"
}
```

## ⚙️ Configuration

### 🔧 Customize PBKDF2 Iterations

The default PBKDF2 iterations (1,200,000) provide excellent security. For custom security levels:

```bash
# Run with custom iterations (example: 1,000,000)
docker run --rm -p 8000:8000 \
  -e secure_qrcode_pbkdf2_iterations=1000000 \
  allisson/secure-qrcode
```

> 💡 **Tip**: Higher iterations = better security but slower performance. Find your balance! ⚖️

## 🤝 Contributing

We welcome contributions! Please feel free to submit issues, feature requests, or pull requests. 🛠️

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 📋

---

**Made with ❤️ for secure data sharing**
