===============
django-tortoise
===============

integration of tortoise orm in django


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


* Free software: GNU General Public License v3
* Documentation: https://django-tortoise.readthedocs.io.

Features
--------

* Pending :D

Demo
----

To run an example project for this django reusable app, click the button below and start a demo serwer on Heroku

.. image:: https://www.herokucdn.com/deploy/button.png
    :target: https://heroku.com/deploy
    :alt: Deploy Django Opt-out example project to Heroku


Quickstart
----------

Install django-tortoise::

    pip install django-tortoise

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_tortoise.apps.DjangoTortoiseConfig',
        ...
    )

Add django-tortoise's URL patterns:

.. code-block:: python

    from django_tortoise import urls as django_tortoise_urls


    urlpatterns = [
        ...
        url(r'^', include(django_tortoise_urls)),
        ...
    ]


Running Tests
-------------

Does the code actually work?

::

    $ pipenv install --dev
    $ pipenv shell
    $ tox


We recommend using pipenv_ but a legacy approach to creating virtualenv and installing requirements should also work.
Please install `requirements/development.txt` to setup virtual env for testing and development.


Credits
-------

This package was created with Cookiecutter_ and the `wooyek/cookiecutter-django-app`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`wooyek/cookiecutter-django-app`: https://github.com/wooyek/cookiecutter-django-app
.. _`pipenv`: https://docs.pipenv.org/install#fancy-installation-of-pipenv
