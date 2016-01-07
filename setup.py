try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

import versioneer
import sys

config = {
    'description': 'worm is a library for multiprocessing with pandas DataFrames',
    'author': 'Matthew Conley',
    'url': 'https://github.com/mtconley/worm',
    'download_url': 'https://github.com/mtconley/worm.git',
    'author_email': '',
    'version': versioneer.get_version(),
    'install_requires': ['pandas','nose', 'findspark'],
    'packages': find_packages(),
    'name': 'worm'
}

print "system is: " + sys.platform
print ''
print "installing dependencies... "
print config['install_requires']

setup(**config)
