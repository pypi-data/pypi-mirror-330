from setuptools import setup, find_packages

setup(
    name="blackjack-noob",
    version="0.1.0",
    author="Adarsh V H",
    author_email="adarshvh2005@gmail.com",
    description="A Python package for playing Blackjack.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Snapout2/blackjack.git",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
