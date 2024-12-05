from django.db import models
from cats.models import SpyCat


class Mission(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    assigned_cat = models.ForeignKey(SpyCat, related_name='missions', on_delete=models.SET_NULL, null=True, blank=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Target(models.Model):
    mission = models.ForeignKey(Mission, related_name="targets", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    notes = models.TextField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name
