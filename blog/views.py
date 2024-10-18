from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Prefetch
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .models import Post, BlogUser, Comment
from .forms import (
    PostCreateForm,
    BlogUserCreateForm,
    CommentCreateForm,
    ReplyCreateForm,
    CommentsSortForm,
)


def index(request):
    sort_by = request.GET.get("sort_by", "created_at")
    order = request.GET.get("order", "asc")

    sort_order = "" if order == "asc" else "-"

    comments_prefetch = Prefetch(
        "comments",
        queryset=Comment.objects.select_related("user").order_by(
            f"{sort_order}{sort_by}"
        ),
    )

    posts = (
        Post.objects.all().select_related("user").prefetch_related(comments_prefetch)
    )

    form = CommentsSortForm(request.GET or None)

    context = {
        "posts": posts,
        "form": form,
    }

    return render(request, "blog/index.html", context)


@login_required
def add_post(request):
    if request.method == "POST":
        form = PostCreateForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data.get("username")
            user_email = form.cleaned_data.get("email")

            if user_name != request.user.username or user_email != request.user.email:
                form.add_error(None, "Name or email doesn't match with your account.")
            else:
                post = form.save(commit=False)
                post.user = request.user
                post.save()
                return redirect("blog:index")
    else:
        form = PostCreateForm()

    return render(request, "blog/create_post.html", {"form": form})


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        form = CommentCreateForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect("blog:index")
    else:
        form = CommentCreateForm()

    return render(
        request,
        "blog/create_comment.html",
        {"form": form, "post": post},
    )


@login_required
def add_reply(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.method == "POST":
        form = ReplyCreateForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.comment = comment
            reply.save()
            return redirect("blog:index")
    else:
        form = CommentCreateForm()

    return render(
        request,
        "blog/create_reply.html",
        {"form": form, "comment": comment},
    )


class BlogUserCreateView(CreateView):
    user = BlogUser
    form_class = BlogUserCreateForm
    template_name = "blog/user_form.html"
    success_url = reverse_lazy("blog:index")
