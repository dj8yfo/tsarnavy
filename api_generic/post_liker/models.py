from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    """ my Post model """

    title = models.CharField(max_length=250)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("-created",)
