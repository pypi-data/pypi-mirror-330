<h1 align="center">create-nb-app</h1>

<p align="center">An opinionated CLI for creating typesafe Python projects.</p>
<p align="center">
<code>pip install create-nb-app</code>
</p>
<br />

## Usage
Run the following command to create a new project:
1. **Install dependencies:**

Make sure you have [questionary](https://pypi.org/project/questionary/) installed:
```bash
pip install questionary
```
Install create-nb-app:
```bash
pip install create-nb-app
```
2. **Install the Package Locally:**
```bash
pip install -e .
```

3. **Create a new project:**
Run the following command:
```bash
create-nb-app <project-name>
```

## Features
- Git initialization
- Virtual environment creation
- Interactive package selection (mypy, black, flake8, pytest, pre-commit, sphinx)
- Configuration files:
  - .gitignore
  - requirements.txt
  - pyproject.toml (for Black)
  - mypy.ini (if selected)
  - .pre-commit-config.yaml (if selected)
  - CITATION.cff
  - MIT LICENSE
  - README.md


## License
This project is licensed under the MIT License.

