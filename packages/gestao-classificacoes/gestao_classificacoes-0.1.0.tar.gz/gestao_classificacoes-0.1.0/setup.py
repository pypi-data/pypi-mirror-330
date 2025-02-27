from setuptools import setup, find_packages

setup(
    name="gestao_classificacoes",
    version="0.1.0",
    author="Seu Nome",
    author_email="seu.email@example.com",
    description="Sistema de Gestão de Classificações de Alunos",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/a041011/gestao_classificacoes",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
