from setuptools import setup, find_packages
import os


setup(
    name='LambdaUtil',
    version='0.4.3',
    packages=find_packages(),
    description='Python Lambda Utility',
    author='Duke P. Takle',
    author_email='duke.takle@gmail.com',
    install_requires=[
        'boto3',
        'Click',
        'tabulate',
        'PyYAML'
    ],
    entry_points='''
        [console_scripts]
        lambdautil=lambdautil.command:cli
    '''
)
