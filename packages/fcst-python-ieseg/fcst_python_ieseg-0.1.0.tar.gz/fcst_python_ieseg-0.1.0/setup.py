from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="fcst_python_ieseg",
    version="0.1.0",
    author="Your Name",
    author_email="f.diazgonzalez@ieseg.fr",
    description="Python utilities for forecasting (IESEG)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fer44tnh/fcst_python_ieseg",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pandas>=1.0.0",
    ],
)