from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="retractometrics",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy"
    ],
    entry_points={
        "console_scripts": [
            "my_package_run = my_package:run",
        ],
    },
    author="Anoop Reddy Reddy",
    description="A package for bibliometric analysis of retracted papers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="retracted papers, bibliometrics",
    python_requires=">=3.6",
)
