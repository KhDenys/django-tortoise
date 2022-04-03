# -*- coding: utf-8 -*-
from pascal_templates.views import CreateView

from . import models


class SampleView(CreateView):
    model = models.SampleModel
