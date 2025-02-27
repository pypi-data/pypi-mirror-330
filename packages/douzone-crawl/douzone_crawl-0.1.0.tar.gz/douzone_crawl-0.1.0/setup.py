from setuptools import setup, find_packages

setup(
    name="Douzone-crawl",
    version="0.1.0",
    author="choheejin",
    author_email="hjcho1027@douzone.com",
    description="A simple web crawling library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/zozni-douzone/Douzone-crawl.git",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)