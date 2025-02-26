from django.db import models

from .namespace import Namespace


class Property(models.Model):
    namespace = models.ForeignKey(Namespace, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Properties"
        unique_together = [["namespace", "name"]]

    def __str__(self):
        return f"{self.namespace.prefix}:{self.name}"
