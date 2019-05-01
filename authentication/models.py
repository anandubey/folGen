from django.db import models


class Credential(models.Model):
    username = models.OneToOneField('user.User', on_delete=models.CASCADE)
    password_hash = models.CharField(max_length=64, null=False)
    #is_scheduled = models.BooleanField(default=True)

    def __str__(self):
        return self.username.username


"""
class ScheduledAccount(models.Model):
    unique_id = models.CharField(max_length=3, primary_key=True)
    expire_time = models.CharField(max_length=14, null=False)
    type_of_schedule = models.CharField(max_length=1, choices=[('N', 'N'), ('D', 'D')], default='N')

    def __str__(self):
        return self.unique_id

"""