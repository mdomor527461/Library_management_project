from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from . models import UserAccount,UserAdress
from datetime import datetime
class UserRegistrationForm(UserCreationForm):
    gender = forms.CharField(max_length=255)
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    street_address = forms.CharField(max_length=100)
    postal_code = forms.IntegerField()
    city = forms.CharField(max_length=100)
    country = forms.CharField(max_length=100)
    
    class Meta:
        model = User
        fields = ['username','first_name','last_name','password1','password2','email',
                  'gender','birth_date','street_address','postal_code','city','country']
        
    def save(self,commit = True):
        user = super().save(commit = False)
        
        if commit == True:
            user.save()
            gender = self.cleaned_data.get('gender')
            birth_date = self.cleaned_data.get('birth_date')
            street_address = self.cleaned_data.get('street_address')
            postal_code = self.cleaned_data.get('postal_code')
            city = self.cleaned_data.get('city')
            country = self.cleaned_data.get('country')
            
            UserAdress.objects.create(
                user = user,
                street_address = street_address,
                postal_code = postal_code,
                city = city,
                country = country
            )
            
            UserAccount.objects.create(
                user = user,
                gender = gender,
                birth_date = birth_date,
                account_no = 100000 + user.id,
                first_deposit_date = datetime.today()
            )
        return user
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
    
            