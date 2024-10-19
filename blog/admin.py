from django.contrib import admin

from .models import Post, Comment, Reply, BlogUser


admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(BlogUser)
