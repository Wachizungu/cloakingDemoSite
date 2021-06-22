from django.db import models


# Create your models here.
class Fingerprint(models.Model):
    hash = models.CharField(max_length=50, unique=True)
    ip = models.GenericIPAddressField()
    blocked = models.BooleanField(default=True)
    visits = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ('hash',)

    def __str__(self):
        return self.hash
