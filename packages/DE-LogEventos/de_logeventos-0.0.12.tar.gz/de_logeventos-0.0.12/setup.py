from setuptools import setup, find_packages

setup(
    name="DE_LogEventos",  # Nome do pacote
    version="0.0.12",  # Versão inicial
    author="Almri J Gomes",
    author_email="almir.jg@hotmail.com",
    description="Log de eventos em processos",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/DE-DataEng/DE_LogEventos.git",  # Opcional
    packages=find_packages(),  # Busca automaticamente os pacotes
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[],  # Dependências (caso tenha)
)

