import setuptools


with open('README.rst') as readme:
    long_description = readme.read()


setuptools.setup(
    name='django-tortoise',
    version='0.0.1',
    author='KhDenys',
    author_email='KhD01214@outlook.com',
    license='MIT',
    description='Integration of Tortoise orm into a Django project with one line of code',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/KhDenys/django-tortoise',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Development Status :: 2 - Pre-Alpha ',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: PL/SQL',
        'Framework :: AsyncIO',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.0',
        'Framework :: Django :: 4.1',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Database',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
    ],
    keywords=(
        'django '
        'tortoise tortoise-orm'
        'sql postgres psql sqlite aiosqlite psycopg asyncpg relational database orm rdbms object mapper '
        'async asyncio aio '
        'monkey patching monkey-patching'
    ).split(),
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=[
        'django>=3.2',
        'tortoise-orm>=0.19.0,<0.19.2'
    ]
)