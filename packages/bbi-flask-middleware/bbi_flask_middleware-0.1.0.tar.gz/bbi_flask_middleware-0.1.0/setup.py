# setup.py
from setuptools import setup, find_packages

setup(
    name='bbi-flask-middleware',
    version='0.1.0',  # Initial version
    packages=find_packages(),  # Automatically find the packages to include
    description='A custom middleware library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Muhammad Irfan',
    license = 'unlicense',
    author_email='irfanliaquat587@gmail.com',
    url='https://github.com/irfan4002/flask-middleware',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
