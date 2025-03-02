from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="automated-data-analysis",
    version="1.1.1",
    author="Vinith kabilar",
    author_email="vinithkabilar@gmail.com",
    description="Automated Data Analysis Pipeline",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vinith-15",
    packages=find_packages(),
    install_requires=[
        'pandas>=1.0.0',
        'numpy>=1.18.0',
        'openpyxl>=3.0.0'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    keywords='data-analysis automation data-cleaning pandas',
)

