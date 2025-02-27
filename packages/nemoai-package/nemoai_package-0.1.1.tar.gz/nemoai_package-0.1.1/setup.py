from setuptools import setup, find_packages

setup(
    name="nemoai_package",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "sphinx",
        "twine",
        "setuptools",
    ],
)
