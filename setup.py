# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='cache_it',
    version='0.0.1',
    description='Decorators for caching',
    author='Shoji Ihara',
    author_email='shoji.ihara@gmail.com',
    url='http://github.com/shoz/cache_it',
    packages=find_packages(),
    license=open('LICENSE').read(),
    include_package_data=True,
    keywords=['memcached', 'test', 'testing', 'decorators'],
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
    ),
    install_requires=[
        'pylibmc==1.2.3',
        'switchcache==0.1.1'
        'nose==1.3.3',
    ],
    tests_require=['nose'],
    test_suite = 'nose.collector'
)
