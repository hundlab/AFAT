#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from setuptools import setup

install_requires = [
'matplotlib',
'scipy',
'scikit-image',
'sklearn']

setup(name='AFAT',
      version='1.0',
      description='A tool to quantify the amount of fibrosis in Masson’s Trichrome stains',
      author='Thomas Hund',
      author_email='hund.1@osu.edu',
      install_requires=install_requires
      )

