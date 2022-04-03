# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _


class NamedModel(models.Model):
    name = models.CharField(max_length=150, verbose_name=_('name'))
