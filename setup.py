try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import os

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

setup(
    name='davison2000unit',
    version='0.1',
    author='Shailesh Appukuttan',
    author_email='shailesh.appukuttan@unic.cnrs-gif.fr',
    packages=['davison2000unit', 'davison2000unit.tests', 'davison2000unit.capabilities', 'davison2000unit.scores', 'davison2000unit.plots'],
    url='https://github.com/appukuttan-shailesh/davison2000unit',
    license='BSD-3-Clause',
    description='A SciUnit library for testing of models from Davison et al. (2000)',
    long_description="",
    install_requires=['sciunit>=0.2.1']
)
