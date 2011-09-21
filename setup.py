#!/usr/bin/env python
from setuptools import setup, find_packages
from django_selenium import __version__

setup(
    name='django-selenium',
    version=__version__,
    author='Roman Prokofyev',
    author_email='roman.prokofyev@gmail.com',
    maintainer='Roman Prokofyev',
    maintainer_email='roman.prokofyev@gmail.com',
    url='https://github.com/dragoon/django-selenium/',
    download_url='https://github.com/dragoon/django-selenium/',

    description='Django Selenium Integration',
    long_description="A test coverage reporting tool that utilizes "
                     "Ned Batchelder's excellent coverage.py to show how "
                     "much of your code is exercised with your tests.",

    license='Apache License 2.0',
    packages=find_packages(),

    requires=['django (>=1.2)', 'selenium (>= 2.5)'],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing',
        ],
    )
