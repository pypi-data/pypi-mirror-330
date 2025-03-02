from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    readme = fh.read()

setup(
    name="DE_LibUtil",  # Nome do pacote
    version="0.0.38",  # Versão inicial
    author="Almir J Gomes",
    author_email="almir.jg@hotmail.com",
    description="Conector com varias base de dados",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/DE-DataEng/DE_LibUtil.git",  # Opcional
    packages=find_packages(),  # Busca automaticamente os pacotes
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[],  # Dependências (caso tenha)
)