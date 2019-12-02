from django.db import models

# Create your models here.


class ManagerUser(models.Model):
    user_name = models.CharField(max_length=20)
    gender = models.BooleanField(null=True)
    account = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    comment = models.CharField(max_length=100,null=True)
