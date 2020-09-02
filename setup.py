from importlib.machinery import SourceFileLoader
from pathlib import Path

from setuptools import setup

description = "Versioning with Fast API"
readme = Path(__file__).parent / "README.md"
if readme.exists():
    long_description = readme.read_text()
else:
    long_description = (
        description + ".\n\nSee https://arq-docs.helpmanual.io/ for documentation."
    )
# avoid loading the package before requirements are installed:
version = SourceFileLoader("version", "fastapi_versioned/version.py").load_module()

setup(
    name="fastapi_versioned",
    version=version.VERSION,
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    python_requires=">=3.6",
    author="Connor Charles",
    author_email="ccharles.gb@gmail.com",
    url="https://github.com/ccharlesgb/fastapi-versioned",
    license="MIT",
    packages=["fastapi_versioned"],
    zip_safe=True,
    install_requires=[
        "fastapi>0.61.0",
        "pydantic>1",
        "openapi-schema-pydantic==1.1.0",
        "semantic-version>2.8",
    ],
    extras_require={"dev": ["pytest>=6.0.0", "requests>=2.24.0"]},
)
