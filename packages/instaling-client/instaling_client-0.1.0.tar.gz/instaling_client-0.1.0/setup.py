from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="instaling-client",
    version="0.1.0",
    author="Julian Zientkowski",
    author_email="julianzkw1@gmail.com",
    description="A client for automating Instaling.pl language learning sessions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pingwiniu/instaling-client",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.25.0",
        "beautifulsoup4>=4.9.0",
    ],
)
