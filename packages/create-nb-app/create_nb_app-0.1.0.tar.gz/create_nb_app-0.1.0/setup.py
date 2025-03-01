from setuptools import setup, find_packages

setup(
    name="create-nb-app",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "questionary",
    ],
    entry_points={
        "console_scripts": [
            "create-nb-app = create_nb_app.cli:main",
        ],
    },
    author="Nikolai G. Borbe",
    author_email="nikolaiborbe@gmail.com",
    description="An oppinionated CLI for creating typesafe Python projects.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/nikolaiborbe/create-nb-app",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)