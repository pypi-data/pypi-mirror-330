from django.db import models

from .property import Property


class Content(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.property} {self.content}"
