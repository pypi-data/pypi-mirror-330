from setuptools import setup, find_packages

setup(
    name='fairness_ranking',
    version='0.1.0',
    description='A package for generating synthetic data, reranking students based on tolerance, and calculating fairness metrics.',
    author='Mallak Alkhathlan',
    author_email='mnalkhathlan@wpi.edu',
    packages=find_packages(),
    install_requires=[
        'pandas',
    ],
)
