from django import forms
from captcha.fields import CaptchaField
from django.contrib.auth.forms import UserCreationForm

from .models import Post, BlogUser, Comment, Reply

from django_ckeditor_5.widgets import CKEditor5Widget

SORT_CHOICES = [
    ("username", "Username"),
    ("email", "Email"),
    ("created_at", "Created at"),
]

ORDER_CHOICES = [
    ("asc", "Ascending"),
    ("desc", "Descending"),
]


class BlogUserCreateForm(UserCreationForm):

    class Meta:
        model = BlogUser
        fields = ["username", "email", "password1", "password2"]


class PostCreateForm(forms.ModelForm):
    username = forms.CharField(
        max_length=255,
        label="Username",
    )
    email = forms.EmailField(label="Email")
    captcha = CaptchaField(label="Captcha", help_text="Enter the captcha")

    class Meta:
        model = Post
        fields = ["text"]
        widgets = {
            "text": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="comment"
            )
        }


class CommentCreateForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ["text"]
        widgets = {
            "text": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="comment"
            )
        }


class ReplyCreateForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ["text"]
        widgets = {
            "text": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="comment"
            )
        }


class CommentsSortForm(forms.Form):
    sort_by = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False,
        label="Sort by",
    )
    order = forms.ChoiceField(
        choices=ORDER_CHOICES,
        required=False,
        label="Order",
    )


class PostEditForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ["text"]
        widgets = {
            "text": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="comment"
            )
        }


class CommentEditForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ["text"]
        widgets = {
            "text": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="comment"
            )
        }


class ReplyEditForm(forms.ModelForm):

    class Meta:
        model = Reply
        fields = ["text"]
        widgets = {
            "text": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="comment"
            )
        }
