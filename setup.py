#!/usr/bin/env python

from distutils.core import setup

setup(name='pyball',
      version='0.1.0',
      description='handling baseball-reference data in python',
      author='gdifiore',
      author_email='difioregabe@gmail.com',
      url='https://www.github.com/SummitCode/pyball/',
      packages=['dist', 'dist.command'],
     )