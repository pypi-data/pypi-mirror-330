from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="jxon-schema",
    version="0.2.0",
    author="Kenta Aratani",
    author_email="kenta.a.desu@gmail.com",  # Update with actual email
    description="JSON with change tracking - A library for converting between JSON and schemas with change tracking",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CoinEZ-JPN/lib_jxon",  # Update with actual URL
    packages=find_packages(exclude=["tests*"]),
    install_requires=[
        "openai>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "mypy>=1.0.0",
            "twine>=4.0.0",
            "build>=0.10.0",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    keywords="json schema openai structured-data",
    project_urls={
        "Bug Reports": "https://github.com/CoinEZ-JPN/lib_jxon/issues",
        "Source": "https://github.com/CoinEZ-JPN/lib_jxon",
    },
)
