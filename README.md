# Task: Implement Secure Login Challenge-Response System

## Summary

Implement the first step of secure login and user registration for the `login_server` service. This ensures that users are authenticated and registered without ever sending their password over the network. It uses a challenge-response method with encryption to validate identity and store secure credentials.

This task also includes writing clean unit tests using Python and `pytest` to validate behavior.

## Goals

* Create a module that handles login challenge.
* Create a module that handles registration.
* Add utilities to encrypt and compare authentication responses securely.
* Write test cases using `pytest`.
* Provide clear documentation and readable flow for future contributors. (Docstrings using [reST](https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html) format)

## How It Works

### Registration Flow

1. Client chooses a username and password.
2. Client sends the username and plaintext password to the server.
3. Server validates the username is available.
4. Server hashes the password and stores it securely with the username.

### Login Flow

1. Client connects to the server with only the username.
2. Server responds with a random challenge (nonce) and its public key.
3. Client generates its own random challenge.
4. Client encrypts the server's challenge using the password hash.
5. Client sends:
   * Encrypted server challenge
   * Client's own challenge
   * Username
6. Server retrieves the user's stored password hash.
7. Server encrypts its original challenge using that hash and compares the result.
8. If it matches, the server responds with an encrypted version of the client's challenge.
9. If the client can decrypt it correctly, mutual authentication is complete.

## Diagrams

### Registration Flow

```mermaid
sequenceDiagram
    participant Client
    participant Server

    Client->>Server: Sends username + plaintext password
    Server->>Server: Check if username is available
    alt Available
        Server->>Server: Hash password
        Server->>Server: Store username + password hash
        Server-->>Client: Registration success
    else Taken
        Server-->>Client: Registration failed (username taken)
    end
```

### Login Flow

```mermaid
sequenceDiagram
    participant Client
    participant Server

    Client->>Server: Sends username
    Server->>Client: Sends server challenge
    Client->>Client: Generates client challenge
    Client->>Client: Encrypts server challenge using password hash
    Client->>Server: Sends encrypted server challenge, client challenge
    Server->>Server: Retrieves stored password hash
    Server->>Server: Encrypts challenge using stored hash
    Server->>Server: Compare with received encrypted challenge
    alt Match
        Server->>Client: Encrypts and sends client challenge back
    else Mismatch
        Server-->>Client: Authentication failed
    end
    Client->>Client: Decrypts challenge
    alt Match
        Client-->>Server: Authentication success
    else Mismatch
        Client-->>Server: Authentication failed
    end
```

## Tests

Use `pytest`. Ensure the following:

* Each module is tested in isolation.
* Add positive and negative cases (correct and incorrect logins/registrations).
* Mock randomness where needed for predictable tests.

## Notes

* Do not use plain-text passwords anywhere beyond initial transmission for registration.
* Use standard libraries where possible.
* Tests must not rely on live randomness — mock or patch for determinism.
