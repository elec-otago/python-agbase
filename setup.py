# python setup.py develop
from setuptools import setup, find_packages

setup(name='AgBase',
      version='0.1.0',
      description='AgBase server communication library',
      url='http://github.com/elec_otago/python-agbase',
      author='Tim Molteno, Mark Butler',
      install_requires=['requests'],
      license='MPL2',
      packages=['agbase'])
