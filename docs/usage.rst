=====
Usage
=====

To use django-tortoise in a project, add it to your `INSTALLED_APPS`:

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
