from setuptools import find_packages, setup

with open("app/Readme.md", "r") as f:
    long_description = f.read()

setup(
    name="monodikit",
    version="0.0.9",
    description="MonodiKit is a Python library designed to facilitate the analysis and processing of medieval chant documents. It was specifically tailored to handle data in the monodi+ data format as edited by the Corpus Monodicum project. The library offers a set of classes that provide a wide range of functionalities, including parsing and processing of chant documents, exploring their hierarchical structure, managing metadata, generating musical notation, and extracting relevant information.",
    package_dir={"": "app"},
    packages=find_packages(where="app"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/timeipert/MonodiKit",
    author="Tim Eipert & Fabian C. Moss",
    author_email="tim.eipert@uni-wuerzburg.de",
    license="MIT",
    classifiers=[""],
    install_requires=[],
    extra_require={
        "dev": ["twine>=4.0.2"]
    },
    python_requires=">=3.8",
)
