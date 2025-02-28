# -*- coding: utf-8 -*-

# Setup module for the Protocol Buffer project
#
# April 2022

import os
import setuptools

# Pull in the essential run-time requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

# Use the README.rst as the long description.
with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(

    name='im-protobuf',
    version=os.environ.get('GITHUB_REF_SLUG', '2.0.0'),
    author='Alan Christie',
    author_email='achristie@informaticsmatters.com',
    url='https://github.com/informaticsmatters/squonk2-protobuf',
    license='MIT',
    description='Cross-product protocol buffers',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    keywords='protobuf protoc messaging',
    platforms=['any'],

    # Our modules to package
    package_dir={'': 'src/main/proto'},
    packages=['informaticsmatters.protobuf',
              'informaticsmatters.protobuf.accountserver',
              'informaticsmatters.protobuf.common',
              'informaticsmatters.protobuf.datamanager'],

    # Project classification:
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Operating System :: POSIX :: Linux',
    ],

    install_requires=requirements,

    zip_safe=False,

)
