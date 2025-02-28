from setuptools import setup, find_packages

setup(
    name="hmlines",
    version="0.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "hmlines = hmlines:main",
        ],
    },
    description="hmlines (how many lines) - A package for counting lines of code in a project",
    author="wertrar",
    author_email="wert-rar@mail.ru",
)