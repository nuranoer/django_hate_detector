from django.db import models

class Tweet(models.Model):
    content = models.TextField()
    is_hoax = models.BooleanField(default=False)
    emotion = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.content
