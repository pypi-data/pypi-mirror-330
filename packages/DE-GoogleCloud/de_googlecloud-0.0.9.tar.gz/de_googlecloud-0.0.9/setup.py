
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    readme = fh.read()

setup(
    name="DE_GoogleCloud",  # Nome do pacote
    version="0.0.9",  # Versão inicial
    author="Almir J Gomes",
    author_email="almir.jg@hotmail.com",
    description="Pacote de funcionalidades para o GCP",
    long_description="Versão estavel. Efetuas novas consistencias em Upload e Downloads para verificação de "
                     "pastas e arquivos existem, e tambem o timeout=60 para upload e download",
    long_description_content_type="text/markdown",
    url="https://github.com/DE-DataEng/DE_GoogleCloud.git",  # Opcional
    packages=find_packages(),  # Busca automaticamente os pacotes
    keywords=['Cloud','Google',"DataEng", "GCP", "Pacote GCP python", "Almir J Gomes", "almir.jg@hotmail.com"],
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[],  # Dependências (caso tenha)
)
