from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class BlogUser(AbstractUser):
    pass


class CreateMessage(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s_messages",
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def formatted_date(self):
        return self.created_at.strftime("%d.%m.%Y %H:%M")

    def __str__(self):
        return f"{self.created_at} ---- {self.user.username} ---- {self.user.email}"

    class Meta:
        abstract = True
        ordering = ("created_at",)


class Post(CreateMessage):
    pass


class Comment(CreateMessage):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
    )


class Reply(CreateMessage):
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name="replies",
    )

    class Meta:
        verbose_name_plural = "Replies"
