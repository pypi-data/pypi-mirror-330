import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="django-access-logging",
    version="1.0.1",
    description="Django middleware to log all requests and responses to a database.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/ross-sharma/django-access-logging",
    author="Ross Sharma",
    author_email="ross@ross-sharma.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages(where=".", include=(["django_access_logging*"])),
    install_requires=["django"],
    entry_points={
        "console_scripts": []
    },
)
