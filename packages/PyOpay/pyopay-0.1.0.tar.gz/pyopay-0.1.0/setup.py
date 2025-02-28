from setuptools import setup, find_packages

setup(
    name="PyOpay",
    version="0.1.0",
    description="A client library for interacting with the Opay API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Precious Ojogu",
    author_email="nkangprecious26@gmail.com",
    url="https://github.com/Prevz26/Opay-py",
    license="MIT",  # No 'license_files'
    packages=find_packages(),
    install_requires=[
        "requests",
        "pydantic",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
