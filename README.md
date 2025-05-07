# TinyMMO Login Server

>Secure login and registration service for the TinyMMO game using a challenge-response protocol.
> Built with **FastAPI**, **PostgreSQL** and **Redis**.

---

## Overview

This service handles secure user registration and authentication without transmitting plaintext passwords.
It uses a **challenge-response login system** that ensures credentials are never exposed over the network.

Key Features:

* Secure challenge-response authentication using Argon2, HKDF, and ChaCha20-Poly1305
* REST and WebSocket login endpoints
* PostgreSQL-backed user repository
<!-- * Full test suite with `pytest` will be in future-->

---

## Installation

### Requirements

* Docker
* Make (optionally)

### Clone the Repo

```bash
git clone https://github.com/Perchinka/TinyMMO_login_server.git
cd TinyMMO_login_server
```

### Local Installation (with Poetry)

```bash
poetry install
cp .env-example .env
```

### Docker Setup (Recommended)

```bash
make run  # or manually:
docker-compose up --build
```

---

## 📂 Project Structure

```
login_server/
🔹 api/                  # FastAPI routes, schemas, WebSocket handlers
🔹 common/               # Shared utilities (logging, exceptions)
🔹 config.py             # App configuration from environment
🔹 domain/               # Core interfaces and domain models
🔹 infra/                # Implementations for abstract adapters and repositories
🔹 services/             # Business logic for registration and login
🔹 bootstrap.py          # App wiring
🔹 app.py                # FastAPI app factory
```

Test coverage lives in the `tests/` directory, with mirroring submodules.

Documentation and architecture references are in `docs/`.

---

## Running Tests

```bash
make test
```

To ensure deterministic results, randomness is mocked in all tests.

---

## Usage

* **Register:**
  `POST /register` with `{ "username": "user", "password": "plain" }`

* **WebSocket Login:**
  Connect to `ws://host/auth/login`
  Exchange challenge and response following the protocol (see diagrams in `docs/api.md`)


---

## 📄 License

[MIT License](./LICENSE)
© 2025 [Alex Lukin](mailto:aleksei.v.lukin@gmail.com)
