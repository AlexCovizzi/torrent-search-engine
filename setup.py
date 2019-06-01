from setuptools import setup, find_packages

requirements = [
    "requests~=2.22",
    "beautifulsoup4~=4.7",
    "jsonschema~=3.0"
]

requirements_dev = [
    "pep8",
    "pytest"
]

setup(
    name="TorrentSearchEngine",
    version="1.0",
    packages=find_packages(exclude="tests"),
    python_requires=">=3.5",
    install_requires=requirements,
    extras_require={
        "dev": requirements_dev
    }
)
