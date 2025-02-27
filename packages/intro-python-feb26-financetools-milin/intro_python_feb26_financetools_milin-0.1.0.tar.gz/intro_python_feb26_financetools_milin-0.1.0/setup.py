from setuptools import setup, find_packages


setup(
  name='intro-python-feb26_financetools_milin',
  version='0.1.0',
  packages=find_packages(),
  install_requires=[
    'numpy',
    'pandas'
  ],
  author='Milin Dalal',
  description=""",
  A collection of finance tools for calculating investment returns and risk assessment.
  """,
  license='MIT',
)