from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
setup(
    name="EvalXAI",
    version="0.1.1",
    description="NLP Explainability Benchmarking Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Kafaite Zahra Hussain",
    author_email="kafait.e.zahra@gmail.com",
    url="https://github.com/kafaite24/EvalXAI",
    packages=find_packages(include=["evalxai", "evalxai.*"]),  # Explicitly include subpackages
    install_requires=[
        "torch",
        "transformers",
        "captum",
        "scikit-learn",
        "matplotlib",
        "datasets",
        "numpy",
        "pandas",
        "seaborn",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)