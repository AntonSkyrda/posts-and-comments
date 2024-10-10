from django.db import models


class CreateMessage(models.Model):
    user_name = models.CharField(max_length=255)
    user_email = models.EmailField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_name} ---- {self.user_email}"

    class Meta:
        abstract = True


class Post(CreateMessage):
    pass


class Comment(CreateMessage):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
