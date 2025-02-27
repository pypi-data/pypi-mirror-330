from setuptools import setup, find_packages

setup(
    name="pyky",
    version="1.0.2",
    author="Erhan",
    author_email="erhan@example.com",
    description="A Python implementation of Kyber Post-Quantum KEM",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/asdfjkl/pyky",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "numpy",
        "pycryptodome"
    ],
    python_requires=">=3.7",
)
