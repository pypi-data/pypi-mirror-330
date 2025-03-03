import sys
import questionary
from .scaffolder import scaffold_project

def interactive_package_selection():
    # Define the ordered list of packages with initial check states.
    choices = [
        questionary.Choice("mypy", checked=True),
        questionary.Choice("black", checked=True),
        questionary.Choice("flake8", checked=False),
        questionary.Choice("pytest", checked=False),
        questionary.Choice("pre-commit", checked=False),
        questionary.Choice("sphinx", checked=False),
    ]
    selected = questionary.checkbox(
        "Select the packages you want to include (use arrow keys or j/k to navigate, space to select, enter to confirm):",
        choices=choices,
    ).ask()
    return selected if selected is not None else []

def main():
    # Get project name from command-line arguments or default to "my_project"
    project_name = sys.argv[1] if len(sys.argv) > 1 else "my_project"
    selected_packages = interactive_package_selection()
    
    print("\nSelected packages:")
    for pkg in selected_packages:
        print(f" - {pkg}")
    
    scaffold_project(project_name, selected_packages)

if __name__ == "__main__":
    main()