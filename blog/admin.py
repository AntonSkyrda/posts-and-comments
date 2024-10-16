from django.contrib import admin

from .models import Post, Comment, BlogUser


admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(BlogUser)
