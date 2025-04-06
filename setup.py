from setuptools import find_packages
from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open('dev.txt') as f:
    requirements_dev = f.read().splitlines()

setup(
    name='cartola_datalake',
    version='0.1.0',
    packages=find_packages(where='cartola_datalake/api'),
    package_dir={'': 'cartola_datalake/api'},
    author='adntayer',
    description='Este projeto tem como objetivo criar um datalake para o CartolaFC',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/adntayer/cartola_datalake',
    install_requires=requirements,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    extras_require={
        'dev': requirements_dev,
    },
)
