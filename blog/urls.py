from django.urls import path

from .views import index, add_post, BlogUserCreateView, add_comment, add_reply

urlpatterns = [
    path("", index, name="index"),
    path("create_posts/", add_post, name="add_post"),
    path("user/create/", BlogUserCreateView.as_view(), name="user_create"),
    path("create_comment/<int:post_id>", add_comment, name="add_comment"),
    path("create_reply/<int:comment_id>", add_reply, name="add_reply"),
]

app_name = "blog"
