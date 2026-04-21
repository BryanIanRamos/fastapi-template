"""Project management commands (Laravel-style)."""

import argparse

from app.db.init_db import run_seed


def main() -> None:
    parser = argparse.ArgumentParser(description="Project management commands")
    parser.add_argument(
        "command",
        choices=["db:seed"],
        help="Command to run (example: db:seed)",
    )

    args = parser.parse_args()

    if args.command == "db:seed":
        run_seed()
        print("Seeder executed")


if __name__ == "__main__":
    main()
