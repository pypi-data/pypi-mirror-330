from setuptools import setup, find_packages

setup(
    name="ibhax",
    version="1.0.0",
    author="Albin Anthony",
    author_email="albin.anthony.dev@gmail.com",
    description="A comprehensive decorator toolkit with 100 production-grade decorators.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ibhax/decorator_factory",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
