from login_server.config import Config
from login_server.app import create_app


def main() -> None:
    config = Config()
    app = create_app(config)

    username = "alice"
    password = "wonderland"

    if app["register"](username, password):
        print(f"Registered user '{username}'")
    else:
        print(f"Registration failed for '{username}'")

    # Simulate login challenge/response
    challenge = app["authenticate"](username, "")
    print(f"Login attempt for '{username}' returned: {challenge}")


if __name__ == "__main__":
    main()
