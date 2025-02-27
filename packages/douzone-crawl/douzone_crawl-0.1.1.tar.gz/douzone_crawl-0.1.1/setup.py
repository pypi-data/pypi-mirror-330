from setuptools import setup, find_packages

setup(
    name="douzone_crawl",
    version="0.1.1",
    author="choheejin",
    author_email="hjcho1027@douzone.com",
    description="A simple web crawling library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/zozni-douzone/douzone_crawl.git",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
)