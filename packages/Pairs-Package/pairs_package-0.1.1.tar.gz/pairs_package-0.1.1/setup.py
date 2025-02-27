from setuptools import setup, find_packages

setup(
    name="Pairs_Package",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        'pandas',
        'pandas_datareader',
        'alpaca-trade-api',
        'numpy',
        'yfinance',
        'python-dotenv',
        'setuptools',
    ],
    description='Pairs Trading strategy, trades executed with Alpaca',
    author='Mihai Posea',
    author_email='pose4408@mylaurier.ca',
    classifiers=[
        'Programming Language :: Python :: 3.8',
    ],
)