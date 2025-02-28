from setuptools import setup, find_packages
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
setup(
    name="hmlines",
    version="0.2",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "hmlines = hmlines:main",
        ],
    },
    description="hmlines (how many lines) - A package for counting lines of code in a project",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="wertrar",
    author_email="wert-rar@mail.ru",
)