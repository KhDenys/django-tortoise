# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _


class SampleModel(models.Model):
    foo = models.CharField(max_length=150, verbose_name=_('foo'))

    class Meta:
        default_related_name = "samples"
        verbose_name = _('sample model')
        verbose_name_plural = _('sample models')
