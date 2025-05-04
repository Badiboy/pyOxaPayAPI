#!/usr/bin/env python
from setuptools import setup
from io import open
import re

def read(filename):
    with open(filename, encoding='utf-8') as file:
        return file.read()

with open('pyOxaPayAPI/version.py', 'r', encoding='utf-8') as f:  # Credits: LonamiWebs
    version = re.search(r"^__version__\s*=\s*'(.*)'.*$",
                        f.read(), flags=re.MULTILINE).group(1)

setup(name='pyOxaPayAPI',
      version=version,
      description='Python implementation of OxaPay (https://oxapay.com) pubilc API',
      long_description=read('README.md'),
      long_description_content_type="text/markdown",
      author='Badiboy',
      url='https://github.com/Badiboy/pyOxaPayAPI',
      packages=['pyOxaPayAPI'],
      requires=['requests'],
      license='MIT license',
      keywords="Crypto Pay API OxaPay",
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Programming Language :: Python :: 3',
          'License :: OSI Approved :: MIT License',
      ],
)
