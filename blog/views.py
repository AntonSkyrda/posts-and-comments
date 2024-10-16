from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .models import Post, BlogUser, Comment
from .forms import (
    MessageCreateForm,
    BlogUserCreateForm,
    CommentCreateForm,
    PostSortForm,
)


def index(request):
    form = PostSortForm(request.GET)
    sort_by = form.cleaned_data["sort_by"] if form.is_valid() else "created_at"

    if sort_by == "username":
        posts = Post.objects.select_related("user").order_by("user__username")
    elif sort_by == "email":
        posts = Post.objects.select_related("user").order_by("user__email")
    else:
        posts = Post.objects.order_by("created_at")

    context = {
        "posts": posts,
        "form": form,
    }

    return render(request, "blog/index.html", context)


@login_required
def add_post(request):
    if request.method == "POST":
        form = MessageCreateForm(request.POST)
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
        form = MessageCreateForm()

    return render(request, "blog/create_post.html", {"form": form})


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    parent_comment = None

    if "parent_id" in request.POST:
        parent_comment = get_object_or_404(Comment, id=request.POST.get("parent_id"))

    if request.method == "POST":
        form = CommentCreateForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            if parent_comment:
                comment.parent = parent_comment
            comment.save()
            return redirect("blog:index")
    else:
        form = CommentCreateForm()

    return render(request, "blog/create_comment.html", {"form": form, "post": post})


class BlogUserCreateView(CreateView):
    user = BlogUser
    form_class = BlogUserCreateForm
    template_name = "blog/user_form.html"
    success_url = reverse_lazy("blog:index")
