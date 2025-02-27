from setuptools import setup, find_packages

setup(
    name='pyutile',
    version='0.1.1',
    description='Collection of essential utilities across development and deployment',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='DirtyWork Solutions Limited',
    author_email='pyutile@open.dirtywork.solutions',
    url='https://github.com/DirtyWork-Solutions/pyutil',
    packages=find_packages(),
    package_dir={},
    install_requires=[
        'pip~=25.0',
        'setuptools~=75.8.0',
        'wheel~=0.45.1',
        'configparser~=7.1.0',
        'loguru~=0.7.3',
        'pyyaml~=6.0.2',
        'omegaconf~=2.3.0'
    ],
)