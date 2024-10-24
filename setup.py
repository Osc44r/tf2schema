import pathlib

from setuptools import setup, find_packages

path = pathlib.Path(__file__).parent

README = (path / "README.md").read_text()

setup(
    name="tf2schema",
    version="0.2.3",
    description="A Python package to interact with the Team Fortress 2 Schema",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Osc44r",
    url="https://github.com/Osc44r/tf2schema/",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=[
        "Team Fortress 2",
        "TF2",
        "Steam",
        "Schema",
        "API",
    ]
)
