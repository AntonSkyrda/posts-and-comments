from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Prefetch
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .models import Post, BlogUser, Comment, Reply
from .forms import (
    PostCreateForm,
    BlogUserCreateForm,
    CommentCreateForm,
    ReplyCreateForm,
    CommentsSortForm,
    PostEditForm,
    CommentEditForm,
    ReplyEditForm,
)
from .utils import clean_and_validate_html


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
                post_text = form.cleaned_data.get("text")

                if post_text:
                    cleaned_text = clean_and_validate_html(post_text)
                    if cleaned_text:
                        post = form.save(commit=False)
                        post.user = request.user
                        post.text = cleaned_text
                        post.save()
                        return redirect("blog:index")
                    else:
                        form.add_error(None, "Your content contains invalid HTML tags.")
                else:
                    form.add_error("text", "Content cannot be empty.")
    else:
        form = PostCreateForm()

    return render(request, "blog/create_post.html", {"form": form})


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        form = CommentCreateForm(request.POST)
        if form.is_valid():
            comment_text = form.cleaned_data.get("text")
            cleaned_text = clean_and_validate_html(comment_text)
            if cleaned_text:
                comment = form.save(commit=False)
                comment.user = request.user
                comment.post = post
                comment.text = cleaned_text
                comment.save()
                return redirect("blog:index")
            else:
                form.add_error(None, "Your comment contains invalid HTML tags.")
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
            reply_text = form.cleaned_data.get("text")
            cleaned_text = clean_and_validate_html(reply_text)
            if cleaned_text:
                reply = form.save(commit=False)
                reply.user = request.user
                reply.comment = comment
                reply.text = cleaned_text
                reply.save()
                return redirect("blog:index")
            else:
                form.add_error(None, "Your reply contains invalid HTML tags.")
    else:
        form = ReplyCreateForm()

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


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.user:
        return HttpResponseForbidden("You do not have permission to delete this post.")

    if request.method == "POST":
        post.delete()
        return redirect("blog:index")
    return render(request, "blog/delete_post.html", {"post": post})


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user != comment.user:
        return HttpResponseForbidden(
            "You do not have permission to delete this comment."
        )

    if request.method == "POST":
        comment.delete()
        return redirect("blog:index")
    return render(request, "blog/delete_comment.html", {"comment": comment})


@login_required
def delete_reply(request, reply_id):
    reply = get_object_or_404(Reply, id=reply_id)
    if request.user != reply.user:
        return HttpResponseForbidden("You do not have permission to delete this reply.")

    if request.method == "POST":
        reply.delete()
        return redirect("blog:index")
    return render(request, "blog/delete_comment.html", {"reply": reply})


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user != post.user:
        return redirect("blog:index")

    if request.method == "POST":
        form = PostEditForm(request.POST, instance=post)
        if form.is_valid():
            post_text = form.cleaned_data.get("text")
            cleaned_text = clean_and_validate_html(post_text)
            if cleaned_text:
                post.text = cleaned_text
                form.save()
                return redirect("blog:index")
            else:
                form.add_error(None, "Your content contains invalid HTML tags.")
    else:
        form = PostEditForm(instance=post)

    return render(request, "blog/edit_post.html", {"form": form})


@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.user != comment.user:
        return redirect("blog:index")

    if request.method == "POST":
        form = CommentEditForm(request.POST, instance=comment)
        if form.is_valid():
            comment_text = form.cleaned_data.get("text")
            cleaned_text = clean_and_validate_html(comment_text)
            if cleaned_text:
                comment.text = cleaned_text
                form.save()
                return redirect("blog:index")
            else:
                form.add_error(None, "Your comment contains invalid HTML tags.")
    else:
        form = CommentEditForm(instance=comment)

    return render(request, "blog/edit_comment.html", {"form": form})


@login_required
def edit_reply(request, reply_id):
    reply = get_object_or_404(Reply, id=reply_id)

    if request.user != reply.user:
        return redirect("blog:index")

    if request.method == "POST":
        form = ReplyEditForm(request.POST, instance=reply)
        if form.is_valid():
            reply_text = form.cleaned_data.get("text")
            cleaned_text = clean_and_validate_html(reply_text)
            if cleaned_text:
                reply.text = cleaned_text
                form.save()
                return redirect("blog:index")
            else:
                form.add_error(None, "Your reply contains invalid HTML tags.")
    else:
        form = ReplyEditForm(instance=reply)

    return render(request, "blog/edit_reply.html", {"form": form})
