from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="terminal-controller-uvx",
    version="0.1.4",
    author="UVx Project",
    author_email="info@uvx.org",
    description="A terminal controller MCP server for UVx",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GongRzhe/terminal-controller-uvx",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "terminal-controller=terminal_controller:main",
        ],
    },
)
