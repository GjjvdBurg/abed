import os

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

setup(
        name = "abed",
        version = "0.0.2",
        author = "Gertjan van den Burg",
        author_email = "gertjanvandenburg@gmail.com",
        description = ("A utility for Automated BEnchmark Distribution"),
        license = "GPL v2",
        packages = find_packages(),
        long_description = read('README.rst'),
        scripts = ['bin/abed'],
        install_requires = [
            'Fabric3==1.12.0.post1',
            'mpi4py==1.3.1',
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
