from django import forms

from movie.models import Review, RATE_CHOICES

class RateForm(forms.ModelForm):
    """docstring for RateForm."""
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'materialize-textarea'}), required=True)
    rate = forms.ChoiceField(choices=RATE_CHOICES, widget=forms.Select(), required=True)

    class Meta:
        model = Review
        fields = ('text', 'rate')
