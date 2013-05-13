from setuptools import setup

from django_anger import __version__


setup(
    name = "django-anger",
    version = __version__,
    packages = ["django_anger"],

    # metadata for upload to PyPI
    author = "Constantin Berzan",
    author_email = "cberzan@gmail.com",
    description = "tools and hacks for using Django _in anger_",
    # long_description = 
    license = "MIT",
    keywords = "django south migration migrations",
    url = "https://github.com/cberzan/django-anger",
    # download_url =

    classifiers = [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
    ],
)
