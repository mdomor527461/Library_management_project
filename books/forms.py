from django import forms
from . import models

class ReviewForm(forms.ModelForm):
    class Meta:
        model = models.ReviewModel
        fields = ['name','body']