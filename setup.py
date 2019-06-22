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

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="TorrentSearchEngine",
    version="1.0.0",
    author="Alex Covizzi",
    description="Search torrents from your favourite websites",
    long_description=long_description,
    url="https://github.com/AlexCovizzi/torrent-search-engine",
    packages=find_packages(exclude="tests"),
    python_requires=">=3.5",
    install_requires=requirements,
    extras_require={
        "dev": requirements_dev
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License"
        "Operating System :: OS Independent",
    ],
)
