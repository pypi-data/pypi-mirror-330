import os
from setuptools import setup, find_packages

# Garante que README.md seja lido corretamente
def read_file(filename):
    """Utility function to read the README file."""
    return open(filename, encoding="utf-8").read() if os.path.exists(filename) else ""

setup(
    name="sagace",
    version="0.1.1",
    description="SAGACE Package - Auxiliary package for developing integrations with the SAGACE system.",
    long_description=read_file("README.md"),
    long_description_content_type="text/markdown",
    author="Ampere Consultoria Empresaria LTDA",
    author_email="desenvolvimento@ampereconsultoria.com.br",
    url="https://gitlab.com/ampere.consultoria/sagace-python-sdk.git",
    packages=find_packages(exclude=["tests", "docs"]),
    install_requires=[
        # Adicione dependências necessárias aqui, exemplo:
        # "requests>=2.26.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
    ],
    python_requires=">=3.7",
    license="MIT",
    keywords="sagace, energy, integrations, ampere",
    entry_points={
        "console_scripts": [
            # Exemplo de comando CLI se necessário
            # "sagace-cli=sagace.cli:main",
        ],
    },
)
