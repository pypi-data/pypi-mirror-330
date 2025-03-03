# myprojectgen/config.py

GITIGNORE_CONTENT = """
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Virtual environment
venv
venv/
.env

# Distribution / packaging
*.egg-info/
dist/
build/
.mypy_cache
.mypy_cache/

# Pytest cache
.pytest_cache
pytest_cache/
.cache/
"""

# Mapping of package names to their pip names (no versions pinned)
REQUIREMENTS_PACKAGES = {
    "mypy": "mypy",
    "black": "black",
    "flake8": "flake8",
    "pytest": "pytest",
    "pre-commit": "pre-commit",
    "sphinx": "sphinx",
}

PYPROJECT_TOML_CONTENT = """
[tool.black]
target-version = ["py38"]
line-length = 140
"""

MYPY_INI_CONTENT = """
[mypy]
python_version = 3.8
warn_return_any = True
disallow_untyped_defs = True
disallow_incomplete_defs = True
check_untyped_defs = True
strict_optional = True
warn_unused_ignores = True
incremental = True
disallow_any_unimported = True
disallow_any_expr = True
disallow_any_decorated = True
disallow_any_generics = True
"""

PRE_COMMIT_CONFIG_CONTENT = """
repos:
  - repo: https://github.com/psf/black
    rev: stable
    hooks:
      - id: black
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v0.910
    hooks:
      - id: mypy
  - repo: https://gitlab.com/pycqa/flake8
    rev: 3.9.2
    hooks:
      - id: flake8
"""

CITATION_CFF_CONTENT = """
cff-version: 1.2.0
message: "If you use this project, please cite it using the following metadata."
title: "MyProject Generator"
authors:
  - family-names: "Doe"
    given-names: "John"
date-released: "2025-02-28"
version: "0.1.0"
"""

MIT_LICENSE_CONTENT = """
MIT License

Copyright (c) [Year] [Author]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

README_CONTENT = """
# {project_name}

This project was generated with [create-np-app](https://github.com/nikolaiborbe/create-nb-app).

## Features

- **Git Repository:** Automatically initialized.
- **Virtual Environment:** An isolated environment created in `venv/`.
- **Selected Tools:** 
    - Static Type Checking with mypy.
    - Code Formatting with Black.
    - Linting with Flake8.
    - Testing with pytest.
- **Pre-commit Hooks:** Configured to run checks before commits.
- **Additional Files:** CITATION.cff and MIT License.

## Testing with pytest

To run tests, simply execute:

```bash
pytest
```
This will discover and run all tests in the tests/ directory.

## Linting with Flake8

Flake8 checks your code for style and programming errors. For example, it will warn you if you have an unused variable or formatting issues.

### Getting Started
1. Activate your virtual environment:
- On Unix/macOS: ```source venv/bin/activate```
- On Windows: ```venv\\Scripts\\activate```
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Start coding! 🚀
""" 