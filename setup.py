import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def get_data_files():
    folder = './data'
    datafiles = []
    for root, dirs, files in os.walk(folder):
        if not dirs:
            newfiles = [root + os.sep + f for f in files]
            datafiles.append((root, newfiles))
    return datafiles

setup(
        name = "abed",
        version = "0.0.1.dev0",
        author = "Gertjan van den Burg",
        author_email = "gertjanvandenburg@gmail.com",
        description = ("A utility for Automated BEnchmark Distribution"),
        license = "GPL v2",
        packages = ['abed', 'abed.results'],
        long_description = read('README.md'),
        scripts = ['bin/abed'],
        install_requires = [
            'fabric',
            'mpi4py',
            'tabulate',
            'bz2file',
            'progressbar'
            ],
        data_files = get_data_files()
)
