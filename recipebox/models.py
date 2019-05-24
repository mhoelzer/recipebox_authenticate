from django.db import models
from django.contrib.auth.models import User


# all classes go here
class Author(models.Model):
    name = models.CharField(max_length=50)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    bio = models.TextField()
    favorites = models.ManyToManyField("Recipe", symmetrical=False, blank=True, related_name="favorites")

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    time_required = models.CharField(max_length=20, null=True)
    instructions = models.TextField()

    def __str__(self):
        return self.title

# Make two form models (contained within forms.py) that we can serve and take in data from.
