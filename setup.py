import os
import re

from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def get_data_files():
    datadir = os.path.join('share', 'data')
    datafiles = []
    for root, dirs, files in os.walk(datadir):
        if not dirs:
            newfiles = [os.path.join(root, f) for f in files]
            datafiles.append((root, newfiles))
    return datafiles

version = re.search('__version__ = "([^\']+)"', 
        open('abed/__init__.py').read()).group(1)

setup(
        name = "abed",
        version = version,
        author = "Gertjan van den Burg",
        author_email = "gertjanvandenburg@gmail.com",
        description = ("A utility for Automated BEnchmark Distribution"),
        license = "GPL v2",
        packages = find_packages(),
        long_description = read('README.rst'),
        scripts = ['bin/abed'],
        install_requires = [
            'Fabric3==1.14.post1',
            'mpi4py',
            'tabulate',
            'bz2file',
            'progressbar',
            'dominate',
            'tqdm',
            'backports.lzma',
            'gitpython'
            ],
        data_files = get_data_files()
)
