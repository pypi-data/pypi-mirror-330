from pathlib import Path
from setuptools import setup, find_packages

setup(
    name="mcmc-estimator",
    version="0.0.1",
    description="Estimates a function's parameters using Metropolis-Hastings to fit data.",
    long_description=(Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/nickgerend/mcmc-estimator",
    author="Nick Gerend",
    author_email="nickgerend@gmail.com",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
    ],
    packages=find_packages(),
    install_requires=["numpy", "matplotlib"],
    include_package_data=True,
    package_data={'': ['data/*.csv']},
)