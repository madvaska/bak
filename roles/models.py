from django.db import models

# Create your models here.
class StandartRole(models.Model):
    # TODO: Define fields here
    mayReadMyAnalyzes = models.BooleanField(default=True)
    mayReadAnalyzesByMyProject = models.BooleanField(default=True)
    mayReadAllAnalyzes = models.
    class Meta:
        verbose_name = 'StandartRole'
        verbose_name_plural = 'StandartRoles'

    def __unicode__(self):
        pass
    def __str__(self):
        pass
