from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="github-repository-manager",
    version="0.1.1",
    author="conficiusa",
    author_email="addawebadua@example.com",
    description="A CLI tool to manage GitHub repositories with interactive features",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/conficiusa/github-repository-manager",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests",
        "blessed",
    ],
    entry_points={
        "console_scripts": [
            "github-repository-manager=github_repo_manager:cli_main",
        ],
    },
)