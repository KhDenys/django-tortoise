===============
django-tortoise
===============

This python package is the simplest way to use Tortoise ORM in an existing (maybe not)
Django project that uses sqlite or PostgreSQL databases


.. image:: https://img.shields.io/pypi/v/django-tortoise.svg
        :target: https://pypi.python.org/pypi/django-tortoise



.. image:: https://readthedocs.org/projects/django-tortoise/badge/?version=latest
        :target: https://django-tortoise.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status
.. image:: https://coveralls.io/repos/github/KhDenys/django-tortoise/badge.svg?branch=develop
        :target: https://coveralls.io/github/KhDenys/django-tortoise?branch=develop
        :alt: Coveralls.io coverage

.. image:: https://codecov.io/gh/KhDenys/django-tortoise/branch/develop/graph/badge.svg
        :target: https://codecov.io/gh/KhDenys/django-tortoise
        :alt: CodeCov coverage

.. image:: https://api.codeclimate.com/v1/badges/0e7992f6259bc7fd1a1a/maintainability
        :target: https://codeclimate.com/github/KhDenys/django-tortoise/maintainability
        :alt: Maintainability

.. image:: https://img.shields.io/github/license/KhDenys/django-tortoise.svg
        :target: https://github.com/KhDenys/django-tortoise/blob/develop/LICENSE
        :alt: License

.. image:: https://img.shields.io/twitter/url/https/github.com/KhDenys/django-tortoise.svg?style=social
        :target: https://twitter.com/intent/tweet?text=Wow:&url=https://github.com/KhDenys/django-tortoise
        :alt: Tweet about this project

.. image:: https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg
        :target: https://saythanks.io/to/KhDenys

..
    * Documentation: https://django-tortoise.readthedocs.io.

Features
--------

* Saving all Django ORM advantages (migrations - the biggest one)
* Monkey patching existing Django models with generated on-the-fly Tortoise ORM models
* Generated Tortoise ORM models have the same behavior as Django models (fields behavior)
* Support all Django models fields and validators added to them (except FileFiled, FilePathField, ImageField)
* Support default database only (DATABASES['default'] from the setting.py)
* You can use Django models or Tortoise ORM models when you want (use Django models when it's more suitable than usage of Tortoise ORM models)
* There are enough limitations that are not described here, so most likely some thing is not supported (pre-alpha release =)
* Easy to use - just one line of code... Okay, two ;)


Quickstart
----------

Install django-tortoise::

    pip install django-tortoise

Modify the asgi.py in the main Django project folder:

.. code-block:: python

    import os

    from django.core.asgi import get_asgi_application
    from django_tortoise.asgi import get_boosted_asgi_application  # first line

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')

    application = get_asgi_application()

    # get_boosted_asgi_application function monkey patch all registered apps models;
    # each model will has abjects attribute (the objects attribute was not modified),
    # which is a Tortoise model actually
    application = get_boosted_asgi_application(application)  # second line

Now you can use all valid Tortoise ORM queries via <model>.abjects attribute:

.. code-block:: python

    await ModelA.abjects.get(id=id)


Running Tests
-------------

::

    $ tox
