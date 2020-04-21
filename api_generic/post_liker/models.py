from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class LikingActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return "{} likes {} at {}".format(self.user, self.post, self.created)


class Post(models.Model):
    """ my Post model """

    title = models.CharField(max_length=250)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    users_like = models.ManyToManyField(
        User, related_name="posts_liked", through=LikingActivity
    )

    def __str__(self):
        return f'{self.title} [{self.id}]'

    class Meta:
        ordering = ("-created",)


class Action(models.Model):
    user = models.ForeignKey(
        "auth.User", related_name="actions", db_index=True, on_delete=models.CASCADE
    )
    verb = models.CharField(max_length=255)
    target_ct = models.ForeignKey(
        ContentType,
        blank=True,
        null=True,
        related_name="target_objs",
        limit_choices_to=(models.Q(model="user") | models.Q(model="post")),
        on_delete=models.CASCADE,
    )
    target_id = models.PositiveIntegerField(null=True, blank=True, db_index=True)
    target = GenericForeignKey("target_ct", "target_id")
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f'{self.user} {self.verb} {self.target} at {self.created}'

    class Meta:
        ordering = ("-created",)
