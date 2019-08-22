#!/usr/bin/env python

from setuptools import setup, find_packages

def readme():
    with open('README.rst') as file:
        return file.read()

setup(name='pidmanager',
      version='1.0',
      description='Module for managing PID files for Python scripts',
      long_description='Module for creating, managing, deleting PID files for Python scripts, inclduing management of old PID files without a current matching process',
      classifiers=[
          'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
          'Development Status :: 5 - Production/Stable',
          'Programming Language :: Python :: 3.6',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Utilities',
      ],
      keywords='PID pid pidfile',
      author='Cortney T. Buffington',
      author_email='n0mjs@me.com',
      install_requires=['psutil>=5.6.3'],
      license='GPLv3',
      url='https://github.com/n0mjs710/pidmanager',
      packages=find_packages()
     )
