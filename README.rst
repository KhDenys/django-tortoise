===============
django-tortoise
===============

This python package is the simplest way to use Tortoise ORM in an existing (maybe not)
Django project that uses sqlite or PostgreSQL databases


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
