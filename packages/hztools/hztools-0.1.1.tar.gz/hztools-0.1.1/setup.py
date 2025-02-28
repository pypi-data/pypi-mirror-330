from setuptools import setup, find_packages

setup(
    name='hztools',
    version='0.1.1',
    description='A Python package for qinfeng only',
    author='qinfeng',
    author_email='Reqinfeng2008@gmail.com',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.18.0',
        'scipy>=1.10.1'
    ]
)