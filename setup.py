"""Setup script for fin."""
from setuptools import setup

setup(
    name="fin",
    version='0.1',
    py_modules=['report'],
    install_requires=[
        'Click',
        'pytest',
        'pytest-coverage',
    ],
    entry_points='''
        [console_scripts]
        fin=fin:fin
    ''',
)
