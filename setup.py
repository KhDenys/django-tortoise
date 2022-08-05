from glob import glob
from os.path import basename, splitext


try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup


setup(
    name='django_tortoise',
    version='0.1.0',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    python_requires='>=3.9',
    install_requires=[
        'django>=3.2',
        'tortoise-orm>=0.19'
    ]
)
