from setuptools import setup, find_packages

setup(
    name="monochrome_dionny",
    version="0.0.3",
    author="Dionny",
    description="Transformar as cores de uma imagem em tons de cinza ou binarizadas em preto e branco",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pillow",
    ],
)
