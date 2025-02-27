from setuptools import find_packages, setup

setup(
    name='onlive_mq',
    version='0.2.0',
    description='Message Service for Onlive',
    author='Alejandro Vargas',
    author_email='alejandro.alfonso@onlive.site',
    packages=find_packages(),
    install_requires=[
        'aio-pika>=6.8.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)