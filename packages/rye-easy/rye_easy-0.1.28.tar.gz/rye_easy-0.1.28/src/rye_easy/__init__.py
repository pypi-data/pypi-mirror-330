import argparse
import subprocess
import shutil
import sys
from pathlib import Path
import tomli
import tomli_w


def get_version():
    """Get current version from rye"""
    result = subprocess.run(["rye", "version"], capture_output=True, text=True)
    return result.stdout.strip()


def clean_dist():
    """Clean dist directory"""
    dist_path = Path("dist")
    if dist_path.exists():
        shutil.rmtree(dist_path)


def update_pyproject(key=None, value=None, section=None):
    """Read or update pyproject.toml file
    
    Args:
        key (str, optional): Key to update. If None, returns the entire pyproject.toml content.
        value (any, optional): Value to set for the key. If None, returns the value of the key.
        section (str, optional): Section in pyproject.toml (e.g., "project", "tool.rye"). 
                                If None, assumes key is at the top level.
    
    Returns:
        dict or any: The pyproject.toml content or the value of the specified key
    """
    pyproject_path = Path("pyproject.toml")
    
    if not pyproject_path.exists():
        raise FileNotFoundError("pyproject.toml not found")
    
    # Read the pyproject.toml file
    with open(pyproject_path, "rb") as f:
        pyproject_data = tomli.load(f)
    
    # If no key is provided, return the entire content
    if key is None:
        return pyproject_data
    
    # Navigate to the specified section
    target = pyproject_data
    if section:
        # Handle nested sections like "tool.rye"
        for part in section.split('.'):
            if part not in target:
                target[part] = {}
            target = target[part]
    
    # If only key is provided, return its value
    if value is None:
        return target.get(key)
    
    # Update the value
    target[key] = value
    
    # Write back to the file
    with open(pyproject_path, "wb") as f:
        tomli_w.dump(pyproject_data, f)
    
    return target[key]


def add_script(script_name, script_target):
    """Add a script entry to the [project.scripts] section in pyproject.toml
    
    Args:
        script_name (str): Name of the script to add
        script_target (str): Target module or function for the script
        
    Returns:
        dict: Updated scripts section
    """
    pyproject_path = Path("pyproject.toml")
    
    if not pyproject_path.exists():
        raise FileNotFoundError("pyproject.toml not found")
    
    # Read the pyproject.toml file
    with open(pyproject_path, "rb") as f:
        pyproject_data = tomli.load(f)
    
    # Check if project section exists
    if "project" not in pyproject_data:
        pyproject_data["project"] = {}
    
    # Check if scripts section exists
    if "scripts" not in pyproject_data["project"]:
        pyproject_data["project"]["scripts"] = {}
    
    # Add or update the script entry
    pyproject_data["project"]["scripts"][script_name] = script_target
    
    # Write back to the file
    with open(pyproject_path, "wb") as f:
        tomli_w.dump(pyproject_data, f)
    
    print(f"Added script '{script_name}' with target '{script_target}'")
    return pyproject_data["project"]["scripts"]


def fix_buildsystem(hatchling_version="1.26.3"):
    """Fix build-system requirements in pyproject.toml
    
    Args:
        hatchling_version (str, optional): Version of hatchling to use. Defaults to "1.26.3".
    
    Returns:
        list: Updated build-system requires list
    """
    pyproject_path = Path("pyproject.toml")
    
    if not pyproject_path.exists():
        raise FileNotFoundError("pyproject.toml not found")
    
    # Read the pyproject.toml file
    with open(pyproject_path, "rb") as f:
        pyproject_data = tomli.load(f)
    
    # Ensure build-system section exists
    if "build-system" not in pyproject_data:
        pyproject_data["build-system"] = {}
    
    # Update the requires list with the specified hatchling version
    requires = []
    for req in pyproject_data["build-system"].get("requires", []):
        if not req.startswith("hatchling"):
            requires.append(req)
    
    # Add the specified hatchling version
    requires.append(f"hatchling=={hatchling_version}")
    
    # Update the build-system requires
    pyproject_data["build-system"]["requires"] = requires
    
    # Ensure build-backend is set
    if "build-backend" not in pyproject_data["build-system"]:
        pyproject_data["build-system"]["build-backend"] = "hatchling.build"
    
    # Write back to the file
    with open(pyproject_path, "wb") as f:
        tomli_w.dump(pyproject_data, f)
    
    print(f"Updated build-system requires to: {requires}")
    return requires


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
    
    # Update pyproject command
    update_parser = subparsers.add_parser("update_pyproject", help="Read or update pyproject.toml")
    update_parser.add_argument("--section", help="Section in pyproject.toml (e.g., 'project', 'tool.rye')")
    update_parser.add_argument("--key", help="Key to update or read")
    update_parser.add_argument("--value", help="Value to set for the key")
    
    # Fix build system command
    fix_parser = subparsers.add_parser("fix_buildsystem", help="Fix build-system requirements in pyproject.toml")
    fix_parser.add_argument("--version", default="1.26.3", help="Version of hatchling to use (default: 1.26.3)")
    
    # Add script command
    script_parser = subparsers.add_parser("add_script", help="Add a script entry to pyproject.toml")
    script_parser.add_argument("--name", required=True, help="Name of the script to add")
    script_parser.add_argument("--target", required=True, help="Target module or function for the script")

    args = parser.parse_args()

    if args.command == "build":
        build()
    elif args.command == "publish":
        publish()
    elif args.command == "update_pyproject":
        result = update_pyproject(key=args.key, value=args.value, section=args.section)
        print(result)
    elif args.command == "fix_buildsystem":
        fix_buildsystem(hatchling_version=args.version)
    elif args.command == "add_script":
        add_script(script_name=args.name, script_target=args.target)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()