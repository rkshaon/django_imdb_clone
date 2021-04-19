from django import forms

from comment.models import Comment

class CommentForm(forms.ModelForm):
    """docstring for CommentForm."""
    body = forms.CharField(widget=forms.Textarea(attrs={'class': 'materialize-textarea'}), required=True)

    class Meta:
        model = Comment
        fields = ('body',)
