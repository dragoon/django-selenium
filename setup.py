#!/usr/bin/env python
from setuptools import setup, find_packages
import django_selenium as ds

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
    long_description="Selenium testing integration into Django",

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
