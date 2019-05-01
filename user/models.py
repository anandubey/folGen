from django.db import models


class User(models.Model):
    username = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=40, null=False,)
    unique_id = models.CharField(max_length=3, null=False, unique=True)
    email = models.EmailField(max_length=255, null=False, unique=True)
    followers = models.CharField(max_length=2000, null=True)
    following = models.CharField(max_length=2000, null=True)

    def __str__(self):
        return self.username


class Deleted_UID(models.Model):
    unique_id = models.CharField(max_length=3, primary_key=True)

    def __str__(self):
        return self.unique_id