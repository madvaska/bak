from django.db import models
from .models import Sample

class SampleList(models.Manager):
    def custom_filter(self):
        return super(SampleList,self).get_query_set().order_by("-pk")
