# kwargify_cli/cli.py

import sys

def main():
    """
    Entry point for kwargify-cli.
    This CLI helps in building AI Agents or AI Workflows with the same DX as dbt.
    """
    if len(sys.argv) > 1:
        print("Received arguments:", sys.argv[1:])
    else:
        print("Welcome to kwargify-cli!")
        print("Use --help to see available commands.")

if __name__ == "__main__":
    main()
