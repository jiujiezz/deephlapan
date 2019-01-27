#!/usr/bin/env python
'''
DeepHLApan set up script
'''

import os, sys, re
from setuptools import setup, Extension
from distutils.sysconfig import get_python_inc

NAME = 'deephlapan'
PACKAGE = [NAME]
VERSION = __import__(NAME).__version__
try:
    f = open("requirements.txt", "rb")
    REQUIRES = [i.strip() for i in f.read().decode("utf-8").split("\n")]
except:
    print("'requirements.txt' not found!")
    REQUIRES = list()

incdir = get_python_inc(plat_specific=1)

def path_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            if filename[0] is not '.':  # filter hidden files
                paths.append(os.path.join(re.sub(NAME+'/', '', path), filename))
    return paths

model = path_files(NAME)

def main():
    setup(name=NAME,
        version=VERSION,
        description='Used for predicting high-confidence neoantigens',
        long_description=open('README.md').read(),
        author='Jingcheng Wu',
        author_email='21619014@zju.edu.cn',
        url='https://github.com/',
        packages=PACKAGE,
        package_dir={NAME: NAME},
        package_data={NAME: model},
        scripts=['bin/deephlapan'],
        install_requires=REQUIRES,
        license=open('LICENSE').read()
        )


if __name__ == '__main__':
    main()

