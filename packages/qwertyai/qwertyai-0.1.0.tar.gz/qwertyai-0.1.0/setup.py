from setuptools import setup, find_packages

setup(
    name="qwertyai",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["requests"],
    author="Твоё Имя",
    author_email="твой_email@example.com",
    description="Библиотека для работы с бесплатными нейросетями",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ТВОЙ_GITHUB/qwertyai",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
