from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Taskes(models.Model):
    task_name=models.CharField(max_length=500)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created_date=models.DateTimeField(auto_now_add=True)
    status=models.BooleanField(default=False)

    def __str__(self):
        return self.task_name
        