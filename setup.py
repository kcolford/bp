#!/usr/bin/python

from distutils.core import setup
setup(name='Boil',
      version='0.1.1a2',
      description='A configurable boilerplate generator.',
      author='Kieran Colford',
      author_email='colfordk@gmail.com',
      maintainer='Kieran Colford',
      maintainer_email='colfordk@gmail.com',
      url='https://github.com/kcolford/bp',
      license='GPLv3',
      packages=['boil', 'boil.core'],
      scripts=['bp.py'])
