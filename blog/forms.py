from django import forms
from captcha.fields import CaptchaField
from django.contrib.auth.forms import UserCreationForm

from .models import Post, BlogUser, Comment


SORT_CHOICES = [
    ("username", "Username"),
    ("email", "Email"),
    ("created_at", "Created at"),
]


class BlogUserCreateForm(UserCreationForm):

    class Meta:
        model = BlogUser
        fields = ["username", "email", "password1", "password2"]


class MessageCreateForm(forms.ModelForm):
    username = forms.CharField(
        max_length=255,
        label="Username",
    )
    email = forms.EmailField(label="Email")
    captcha = CaptchaField(label="Captcha", help_text="Enter the captcha")

    text = forms.CharField(
        label="Post's text",
    )

    class Meta:
        model = Post
        fields = ["text"]


class CommentCreateForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ["text"]


class PostSortForm(forms.Form):
    sort_by = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False,
        label="Sort by",
    )
