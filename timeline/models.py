from django.db import models


class Post(models.Model):
    post_id = models.CharField(max_length=14, null=False, primary_key=True)
    post_content = models.CharField(max_length=512, null=False)
    liked_by = models.CharField(max_length=2000, null=True)

    def __str__(self):
        return self.post_id


"""
    Unique post_id is 14 char with format = uid-secondssinceepoch
    from datetime import datetime
    Use int(datetime.now().timestamp()) to get epoch timestamp
    To convert epoch time to human readable, use datetime.fromtimestamp(ts).strftime('%d:%b:%Y %I:%M %p'). ts is the epoch time
    Output format e.g.: 04:Apr:2019 01:36 PM
    
"""