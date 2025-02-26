from setuptools import setup, find_packages

try:
    with open("README.md", "r") as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = ""

setup(
    name="modular-api-mateus",  # Updated to a unique name
    version="0.2.0",  # Version number
    packages=find_packages(where="modular_api"),  # Auto-discover packages inside modular_api
    install_requires=[
        "requests",  # Add other dependencies here
        "python-dotenv",
        "pytest",
        "langchain",
        "openai"
    ],
    author="Mateus Anjos",
    author_email="anjosmat14@gmail.com",
    description="A modular API client for making HTTP requests in Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Anjosmat/modular_api",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
