from setuptools import setup, find_packages

setup(
    name="fuson_strategy_client",
    version="0.1.1",
    description="A Python library to access strategies' results API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Andrew Yu Yang",
    author_email="yang_yu2023@163.com",
    packages=find_packages(),
    install_requires=['requests>=2.25.1'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"],
    python_requires=">=3.6",
)