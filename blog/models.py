from django.db import models


class CreateMessage(models.Model):
    user_name = models.CharField(max_length=255)
    user_email = models.EmailField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def formatted_date(self):
        return self.created_at.strftime("%d.%m.%Y %H:%M")

    def __str__(self):
        return f"{self.user_name} ---- {self.user_email}"

    class Meta:
        abstract = True


class Post(CreateMessage):
    pass


class Comment(CreateMessage):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies",
    )
