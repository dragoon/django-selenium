#!/usr/bin/env python
import os.path

from setuptools import setup, find_packages
import django_selenium as ds

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='django-selenium',
    version=ds.__version__,
    author=ds.__author__,
    author_email=ds.__email__,
    maintainer=ds.__maintainer__,
    maintainer_email=ds.__email__,
    url=ds.__url__,
    download_url=ds.__url__,

    description=ds.__summary__,
    long_description = read('README.rst'),

    license=ds.__license__,
    packages=find_packages(),

    requires=['django (>=1.2)', 'selenium (>= 2.5)'],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing',
        ],
    zip_safe = True
    )
