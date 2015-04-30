import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
        name = "abed",
        version = "0.0.1.dev0",
        author = "Gertjan van den Burg",
        author_email = "gertjanvandenburg@gmail.com",
        description = ("A utility for Automated BEnchmark Distribution"),
        license = "GPL v2",
        packages = ['abed'],
        long_description = read('README.md'),
        scripts = ['bin/abed']
)
