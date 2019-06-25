from setuptools import setup

import os
thelibFolder = os.path.dirname(os.path.realpath(__file__))
requirementPath = thelibFolder + '/REQUIREMENTS.txt'
install_requires = [] # Examples: ["gunicorn", "docutils>=0.3", "lxml==0.5a7"]
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()

setup(
    name='assayconverter',
    version='0.1.0',
    install_requires=install_requires,
    url='https://github.com/michaelchimento/assayconverter',
    license='MIT',
    author='Michael Chimento',
    author_email='',
    description='convert a folder of personality assay scripts (txt) to csv'
)
