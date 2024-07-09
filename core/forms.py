from django import forms
from django.contrib.auth.models import User
from . import models
class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']
        
class DepositeForm(forms.ModelForm):
    class Meta:
        model = models.DepositeModel
        fields = ['amount']
    
    def clean_amount(self):
        min_deposite = 100
        max_deposite = 100000
        
        amount = self.cleaned_data.get('amount')
        
        if amount > max_deposite:
            raise forms.ValidationError(f"you can't deposite greater than {max_deposite}")
        if amount < min_deposite:
            raise forms.ValidationError(f"you can't diposite less than {min_deposite}")
        return amount
        
        