from django.db import models
from django.contrib.auth.models import User
class NotesFile(models.Model):
    title = models.CharField(max_length=256)
    note = models.TextField()
    time = models.DateTimeField()
    username = models.CharField(max_length=100)
    def __str__(self):
        return self.title
