from distutils.core import setup
setup(
  name = 'pyARC',
  packages = ['pyARC'],
  version = '1.0',
  description = 'An implementation of CBA algorithm',
  author = 'Jiří Filip',
  author_email = 'j.f.ilip@seznam.cz',
  url = 'https://github.com/jirifilip/pyARC',
  download_url = 'https://github.com/jirifilip/pyARC/archive/1.0.tar.gz',
  keywords = ['classification', 'CBA', 'association rules', "machine learning"],
  classifiers = [],
  install_requires=['pandas', "fim"]
)