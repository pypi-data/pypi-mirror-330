import argparse
import sys

from .linter import ImportLinter


def main():
    """Main entry point for the import linter command line tool."""
    parser = argparse.ArgumentParser(
        description="Import Linter - Enforce architecture dependencies"
    )
    parser.add_argument(
        "--config",
        "-c",
        default=".importlinter",
        help="Path to the configuration file (default: .importlinter)",
    )
    parser.add_argument(
        "--directory",
        "-d",
        default=None,
        help="Directory to analyze (default: current directory)",
    )

    args = parser.parse_args()
    linter = ImportLinter(args.config)
    success = linter.run(args.directory)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
