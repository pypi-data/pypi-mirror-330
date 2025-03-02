from setuptools import setup, find_packages

setup(name='substitute3',
    version='1.3.0',
    description='A friendly substitute for python mocking frameworks',
    author='Original: Johannes Hofmeister',
    author_email='substitute@spam.cessor.de',
    url='https://github.com/Marcurion/substitute3',
    long_description=open('README.md').read(),  # Optional: read from README.md
    long_description_content_type='text/markdown',  # Specify markdown if used
    packages=find_packages(),
    keywords=['mock','stub','fake','test','testing','tdd','bdd','substitute','substitution','replacement','unittesting'],
    python_requires = '>=3.11.11',  # Minimum version of Python
)