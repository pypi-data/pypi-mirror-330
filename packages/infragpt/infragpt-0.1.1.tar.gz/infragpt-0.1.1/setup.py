from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="infragpt",
    version="0.1.1",
    author="InfraGPT Team",
    author_email="your.email@example.com",
    description="A CLI tool that converts natural language to Google Cloud (gcloud) commands",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/priyanshujain/infragpt",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "infragpt=infragpt:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
        "Topic :: System :: Systems Administration",
    ],
    python_requires=">=3.8",
)