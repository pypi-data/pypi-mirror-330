from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="indoxrouter",
    version="0.1.0",
    author="Ashkan Eskandari",
    author_email="ashkan.eskandari.dev@gmail.com",
    description="Client library for IndoxRouter - A unified API for multiple LLM providers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/indoxRouter",
    packages=find_packages(include=["indoxRouter", "indoxRouter.*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.0",
        "pyjwt>=2.0.0",
    ],
)
