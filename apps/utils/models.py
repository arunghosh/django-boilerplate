from django.db import models


class NameOnlyModelBase(models.Model):
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=64, blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True
        ordering = ['name']


