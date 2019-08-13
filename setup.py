from setuptools import setup

from os import path
from io import open

here = path.abspath(path.dirname(__file__))

"""
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
"""

setup(
  name = 'pyarc',
  packages = ['pyarc', "pyarc.data_structures", "pyarc.algorithms", "pyarc.qcba", "pyarc.utils"],
  version = '1.0.15',
  description = 'An implementation of CBA algorithm',
  #long_description=long_description,
  #long_description_content_type='text/markdown',
  author = 'Jiří Filip',
  author_email = 'j.f.ilip@seznam.cz',
  url = 'https://github.com/jirifilip/pyARC',
  download_url = 'https://github.com/jirifilip/pyARC/archive/1.0.tar.gz',
  keywords = 'classification CBA association rules machine learning',
  classifiers = [],
  install_requires=['pandas', 'numpy', 'sklearn']
)