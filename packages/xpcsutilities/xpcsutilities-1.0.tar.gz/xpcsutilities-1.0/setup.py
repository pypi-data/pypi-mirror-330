#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 17:12:34 2021

@author: opid02
"""

import sys
if sys.version_info < (3,6):
    sys.exit('Sorry, Python < 3.6 is not supported')

from setuptools import setup, find_packages

setup(name='xpcsutilities',
      version='1.0',
      python_requires='>3.6',
      description='ESRF ID02 XPCSUtilities',
      author='William Chèvremont',
      author_email='william.chevremont@esrf.fr',
      install_requires=[
          'numpy',
          'scipy',
          'h5py>=3.4',
          'hdf5plugin',
          'fabio',
          'watchdog',
          'PyQt5',
          'matplotlib',
          'pandas'
      ],
      packages=find_packages(include=['xpcsutilities', 'xpcsutilities.*']),
      entry_points={
                  'console_scripts': ['XPCSUtilities=xpcsutilities.bin.main:main',
                                    ]
              },
      package_data={'': ['xpcsutilities-logo.svg']},
      include_package_data=True,
    )

