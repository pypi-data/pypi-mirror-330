# setup.py

import pathlib
from setuptools import setup, find_packages

setup(
    name='interfusion_encoder',
    version='2.0.6',
    description='A package for training and inference of the InterFusion Encoder model',
    long_description=pathlib.Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    author='Edward Liu',
    author_email='edwardliu01@gmail.com',
    packages=find_packages(),
    install_requires=[
        'torch>=1.7.0',
        'transformers>=4.0.0',
        'numpy',
        'pandas',
        'tqdm',
        'wandb',
    ],
    python_requires='>=3.6',
)

