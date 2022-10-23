from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField()
    likes = models.ManyToManyField(User, related_name="liked", null=True)

    # def serialize(self):
    #     return {
    #         "id": self.id,
    #         "author": self.author.username,
    #         "text": self.text,
    #         "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
    #         "likes": self.likes
    #     }


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed')
