from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="cocoman",
    version="0.3",
    author="wauo",
    author_email="markadc@126.com",
    description="Air Spider",
    packages=find_packages(),
    python_requires=">=3.10",
    long_description=long_description,
    long_description_content_type="text/markdown",
)
