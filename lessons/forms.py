from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    comment = forms.CharField(max_length=1000,
        widget=forms.Textarea(attrs={
            "id": "comment_box",
            "placeholder": "enter your comment",
            "cols": 30,
            "rows": 10
            }))

    class Meta:
        model = Comment
        fields = ['comment']