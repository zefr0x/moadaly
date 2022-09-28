"""A launcher for the application."""
from sys import argv

from .ui import main

if __name__ == "__main__":
    raise SystemExit(main.main(argv))
