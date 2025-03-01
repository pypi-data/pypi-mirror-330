from setuptools import setup, find_packages

setup(
    name="kurlui",
    version="0.2",
    description="A simple UI library inspired by Rayfield",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Xscripts Inc.",
    author_email="sunnyplaysyt9@gmail.com",
    url="",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)