"""
Je définis ici les métadonnées d'installation du projet Paxel.
"""

from setuptools import setup, find_packages

setup(
    name="paxel",
    version="0.1.0",
    author="Badley08",
    description="Assistant Linux en Python avec interface GTK4 et CLI",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Badley08/paxel",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "textual>=0.47.0",
        "psutil>=5.9.0",
    ],
    entry_points={
        "console_scripts": [
            "paxel=paxel.main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Environment :: X11 Applications :: GTK",
        "Topic :: Desktop Environment",
        "Topic :: System :: Systems Administration",
    ],
)
