from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
import tzlocal

class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.name

def get_local_time():
    local_time = tzlocal.get_localzone()
    return datetime.now(local_time)

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(default=get_local_time)
    deadline = models.DateTimeField()
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        return self.title