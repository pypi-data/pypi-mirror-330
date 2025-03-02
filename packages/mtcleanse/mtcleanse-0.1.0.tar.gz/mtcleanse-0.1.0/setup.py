from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mtcleanse",
    version="0.1.0",
    author="Antonio Castaldo",
    author_email="antonio.castaldo@phd.unipi.it",
    description="Machine Translation Corpus Cleaning and Processing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ancastal/mtcleanse",
    project_urls={
        "Bug Tracker": "https://github.com/Ancastal/mtcleanse/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: Linguistic",
    ],
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "numpy>=1.19.0",
        "torch>=1.7.0",
        "scikit-learn>=0.24.0",
        "sentence-transformers>=2.0.0",
        "rich>=10.0.0",
        "tqdm>=4.50.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "isort>=5.0.0",
            "flake8>=6.0.0",
            "build>=0.10.0",
            "twine>=4.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "mtcleanse-clean=mtcleanse.bin.clean_cli:main",
        ],
    },
) 