from django.urls import path

from .views import (
    index,
    add_post,
    BlogUserCreateView,
    add_comment,
    add_reply,
    delete_post,
    delete_comment,
    delete_reply,
    edit_post,
    edit_comment,
    edit_reply,
)

urlpatterns = [
    path("", index, name="index"),
    path("create_posts/", add_post, name="add_post"),
    path("user/create/", BlogUserCreateView.as_view(), name="user_create"),
    path("create_comment/<int:post_id>", add_comment, name="add_comment"),
    path("create_reply/<int:comment_id>", add_reply, name="add_reply"),
    path("delete_post/<int:post_id>", delete_post, name="delete_post"),
    path("delete_comment/<int:comment_id>", delete_comment, name="delete_comment"),
    path("delete_reply/<int:reply_id>", delete_reply, name="delete_reply"),
    path("edit_post/<int:post_id>/", edit_post, name="edit_post"),
    path("edit_comment/<int:comment_id>/", edit_comment, name="edit_comment"),
    path("edit_reply/<int:reply_id>/", edit_reply, name="edit_reply"),
]

app_name = "blog"
