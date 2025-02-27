# rye-easy
[![Rye](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/rye/main/artwork/badge.json)](https://rye.astral.sh)

Rye Easy is a tool to help you manage your Python projects with Rye.

## Installation

```bash
pip install rye-easy
```

## Usage

Rye Easy provides simple commands to build and publish your Python packages managed with Rye.

### Command Line Interface

#### Build Command

```bash
python -m rye_easy build
```

When you run the build command, the following operations are performed:
1. Cleans the `dist` directory to remove any previous build artifacts
2. Bumps the patch version of your package using `rye version --bump patch`
3. Builds the package using `rye build`
4. Installs the newly built wheel package locally using pip

This is useful for testing your package locally before publishing.

#### Publish Command

```bash
python -m rye_easy publish
```

When you run the publish command, the following operations are performed:
1. Bumps the patch version of your package using `rye version --bump patch`
2. Adds the updated `pyproject.toml` to git staging
3. Commits the changes with the message "update version"
4. Creates a git tag with the new version (prefixed with 'v')
5. Pushes the commit to the remote repository
6. Pushes the tags to the remote repository

This command automates the entire release process in one step.

#### Update Pyproject Command

```bash
# Read the entire pyproject.toml
python -m rye_easy update_pyproject

# Read a specific value
python -m rye_easy update_pyproject --section project --key version

# Update a specific value
python -m rye_easy update_pyproject --section project --key description --value "New description"
```

The update_pyproject command allows you to read or modify values in your pyproject.toml file:
- Without arguments, it returns the entire pyproject.toml content
- With `--section` and `--key`, it reads a specific value
- With `--section`, `--key`, and `--value`, it updates a specific value

The section parameter supports nested sections using dot notation (e.g., "tool.rye").

#### Fix Build System Command

```bash
# Use the default hatchling version (1.26.3)
python -m rye_easy fix_buildsystem

# Specify a different hatchling version
python -m rye_easy fix_buildsystem --version 1.27.0
```

The fix_buildsystem command updates the build-system requirements in your pyproject.toml file:
1. Removes any existing hatchling entries from the requires list
2. Adds the specified hatchling version (default is 1.26.3)
3. Ensures the build-backend is set to "hatchling.build"

This is useful for fixing build issues related to the hatchling version.

#### Add Script Command

```bash
# Add a script entry
python -m rye_easy add_script --name my_script --target "my_package.module:function"
```

The add_script command adds or updates a script entry in the [project.scripts] section of your pyproject.toml file:
- `--name`: Name of the script to add
- `--target`: Target module or function for the script

For example, the command above would add the following entry to your pyproject.toml:
```toml
[project.scripts]
my_script = "my_package.module:function"
```

### As a Python Module

```python
from rye_easy import build, publish, update_pyproject, fix_buildsystem, add_script

# Build your package
build()

# Publish your package
publish()

# Read or update pyproject.toml
data = update_pyproject()  # Read entire file
version = update_pyproject(key="version", section="project")  # Read a value
update_pyproject(key="description", value="New description", section="project")  # Update a value

# Fix build system
fix_buildsystem()  # Use default hatchling version (1.26.3)
fix_buildsystem(hatchling_version="1.27.0")  # Specify a version

# Add a script entry
add_script(script_name="my_script", script_target="my_package.module:function")
```

### Functions

- `build()`: Bumps patch version, builds the package, and installs it locally
- `publish()`: Bumps patch version, commits changes, creates a git tag, and pushes to remote
- `clean_dist()`: Cleans the dist directory
- `get_version()`: Gets the current version from Rye
- `update_pyproject(key=None, value=None, section=None)`: Reads or updates values in pyproject.toml
- `fix_buildsystem(hatchling_version="1.26.3")`: Updates build-system requirements in pyproject.toml
- `add_script(script_name, script_target)`: Adds a script entry to the [project.scripts] section

## TODO 
- [x] pyproject.toml hatching 버젼 수정하여 build 잘 되게 하기
- [ ] github action 에서 배포가 잘될 수 있게 .github\workflows\python-publish.yml을 복사할 수 있게 하기 
