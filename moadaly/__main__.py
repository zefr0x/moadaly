"""A launcher for the application."""
from sys import argv

from .ui.main import main_ui


def main() -> int:
    """Entry point for the application."""
    main_ui(argv)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
