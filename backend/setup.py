import pathlib
from setuptools import setup, find_packages

# The directory containing this file
PROJECT_FOLDER = pathlib.Path(__file__).parent.parent

# The text of the README file
README = (PROJECT_FOLDER / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="quatek-web-app",
    version="1.0.0",
    description="quatek web app",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Shun Chen",
    author_email="chenshun@weiguda.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["app"],
    include_package_data=True,
)
