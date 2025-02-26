import argparse
import subprocess
import shutil
import sys
from pathlib import Path


def get_version():
    """Get current version from rye"""
    result = subprocess.run(["rye", "version"], capture_output=True, text=True)
    return result.stdout.strip()


def clean_dist():
    """Clean dist directory"""
    dist_path = Path("dist")
    if dist_path.exists():
        shutil.rmtree(dist_path)


def build():
    """Build package"""
    clean_dist()

    # Bump patch version
    subprocess.run(["rye", "version", "--bump", "patch"], check=True)

    # Get new version
    version = get_version()

    # Build package
    subprocess.run(["rye", "build"], check=True)

    # Install package
    wheel_file = list(Path("dist").glob("*.whl"))[0]
    print(f"Installing the package... {version}")
    subprocess.run(["pip", "install", str(wheel_file)], check=True)


def publish():
    """Publish package"""
    # Bump patch version
    subprocess.run(["rye", "version", "--bump", "patch"], check=True)

    # Get new version
    version = f"v{get_version()}"

    # Git operations
    commands = [
        ["git", "add", "pyproject.toml"],
        ["git", "commit", "-m", "update version"],
        ["git", "tag", version],
        ["git", "push"],
        ["git", "push", "--tags"],
    ]

    for cmd in commands:
        subprocess.run(cmd, check=True)


def main():
    parser = argparse.ArgumentParser(description="Build and publish package")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Build command
    subparsers.add_parser("build", help="Build the package")

    # Publish command
    subparsers.add_parser("publish", help="Publish the package")

    args = parser.parse_args()

    if args.command == "build":
        build()
    elif args.command == "publish":
        publish()
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()


