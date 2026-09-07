from django.db import models


class Chore(models.Model):
    title = models.CharField("title or description", max_length=255)
    responsible_person = models.CharField(max_length=100)
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)
