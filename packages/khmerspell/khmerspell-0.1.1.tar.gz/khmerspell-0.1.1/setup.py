from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

extras_requirements = {
    "test": [
        "pytest",
        "coverage",
    ],
}

setup(
    name="khmerspell",
    version="0.1.1",
    description="Khmer Spelling or Unicode Character Reordering based on the [khmer character specification](https://github.com/sillsdev/khmer-character-specification/blob/master/specification.md).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/maohieng/khmerspell",
    author="Hieng MAO",
    author_email="maohieng@gmail.com",
    license="Apache License 2.0",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Natural Language :: English",
    ],
    packages=find_packages(),
    install_requires=[],
    include_package_data=True,
    python_requires='>=3.5'
)