from setuptools import setup, find_packages
import os

# Читаем содержимое README.md
try:
    with open("README.md", encoding="utf-8") as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = "A powerful cross-platform terminal styling library"

# Читаем requirements-dev.txt если он существует
dev_requirements = []
if os.path.exists("requirements-dev.txt"):
    with open("requirements-dev.txt") as f:
        dev_requirements = [
            line.strip() 
            for line in f 
            if line.strip() and not line.startswith("#")
        ]

setup(
    name="bprinter",
    version="0.1.0",
    author="DGaliaf",
    description="A powerful cross-platform terminal styling library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DGaliaf/bprinter",
    project_urls={
        "Bug Tracker": "https://github.com/DGaliaf/bprinter/issues",
        "Documentation": "https://github.com/DGaliaf/bprinter",
        "Source Code": "https://github.com/DGaliaf/bprinter",
    },
    packages=find_packages(exclude=["tests*", "examples*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Terminals",
        "Topic :: Text Processing",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    keywords="terminal cli ansi-colors text-formatting ascii-art cross-platform console terminal-colors styling markdown logging",
    python_requires=">=3.7",
    install_requires=[
        "pyfiglet>=1.0.2",
    ],
    extras_require={
        "dev": dev_requirements,
    } if dev_requirements else {},
    entry_points={
        "console_scripts": [
            "bprinter=bprinter.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
