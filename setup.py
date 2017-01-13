from os import path
from setuptools import setup, find_packages
import versioneer

here = path.abspath(path.dirname(__file__))

setup(
    name='processors',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),

    description='Data processing library based on pandas and numpy.',
    long_description='Data processing library based on pandas and numpy.',

    url='https://github.com/pa1ko/data-processors',

    author='Patryk Konarzewski',
    author_email='pa.ko@wp.pl',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='data analysis',
    packages=find_packages(exclude=['tests']),
    install_requires=['numpy', 'pandas'],

    # $ pip install -e .[dev]
    extras_require={
        'dev': ['pylint', 'pep8', 'flake8', 'ipython'],
    },

)