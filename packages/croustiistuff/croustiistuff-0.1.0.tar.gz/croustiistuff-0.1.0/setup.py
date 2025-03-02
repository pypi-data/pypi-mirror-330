from setuptools import setup, find_packages

setup(
    name="croustiistuff",
    version="0.1.0",
    author="Croustii",
    author_email="",
    description="Logging package for my need",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
