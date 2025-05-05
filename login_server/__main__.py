from .config import Config
from .app import create_app

def main():
    config = Config()
    app = create_app(config)

if __name__ == "__main__":
    main()
