import os
import subprocess
import sys
from .config import (
    GITIGNORE_CONTENT,
    REQUIREMENTS_PACKAGES,
    PYPROJECT_TOML_CONTENT,
    MYPY_INI_CONTENT,
    PRE_COMMIT_CONFIG_CONTENT,
    CITATION_CFF_CONTENT,
    MIT_LICENSE_CONTENT,
    README_CONTENT,
)

def run_command(command, cwd=None):
    result = subprocess.run(command, shell=True, cwd=cwd)
    if result.returncode != 0:
        print(f"Command failed: {command}")
        sys.exit(1)

def scaffold_project(project_name, selected_packages):
    # Create project directory and change into it
    os.makedirs(project_name, exist_ok=True)
    os.chdir(project_name)
    
    # Initialize Git repository
    run_command("git init")
    print("Initialized git repository.")
    
    # Create .gitignore file
    with open(".gitignore", "w") as f:
        f.write(GITIGNORE_CONTENT.strip())
    print("Created .gitignore.")
    
    # Create virtual environment (works on both Windows and macOS)
    run_command("python -m venv venv")
    print("Created virtual environment.")
    
    # Create requirements.txt (only include packages that were selected)
    reqs = []
    for pkg in selected_packages:
        if pkg in REQUIREMENTS_PACKAGES:
            reqs.append(REQUIREMENTS_PACKAGES[pkg])
    with open("requirements.txt", "w") as f:
        f.write("\n".join(reqs))
    print("Created requirements.txt.")
    
    # Create pyproject.toml for Black configuration
    with open("pyproject.toml", "w") as f:
        f.write(PYPROJECT_TOML_CONTENT.strip())
    print("Created pyproject.toml.")
    
    # Create mypy.ini if mypy was selected
    if "mypy" in selected_packages:
        with open("mypy.ini", "w") as f:
            f.write(MYPY_INI_CONTENT.strip())
        print("Created mypy.ini.")
    
    # Create pre-commit config if pre-commit was selected
    if "pre-commit" in selected_packages:
        with open(".pre-commit-config.yaml", "w") as f:
            f.write(PRE_COMMIT_CONFIG_CONTENT.strip())
        print("Created .pre-commit-config.yaml.")
    
    # Create CITATION.cff file
    with open("CITATION.cff", "w") as f:
        f.write(CITATION_CFF_CONTENT.strip())
    print("Created CITATION.cff.")
    
    # Create MIT LICENSE file
    with open("LICENSE", "w") as f:
        f.write(MIT_LICENSE_CONTENT.strip())
    print("Created LICENSE file.")
    
    # Create README.md file (replacing placeholder with the project name)
    with open("README.md", "w") as f:
        f.write(README_CONTENT.format(project_name=project_name).strip())
    print("Created README.md.")
    
    # Create basic project structure: src/ and tests/ directories
    os.makedirs("src", exist_ok=True)
    os.makedirs("tests", exist_ok=True)
    with open(os.path.join("src", "__init__.py"), "w") as f:
        f.write("# Initial package file")
    print("Created src/ and tests/ directories.")
    
    print(f"\nProject '{project_name}' scaffolded successfully!")