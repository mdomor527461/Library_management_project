from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class UserAccount(models.Model):
    user = models.OneToOneField(User,related_name='account',on_delete= models.CASCADE,null= True)
    
    account_no = models.IntegerField(unique=True)
    gender = models.CharField(max_length=100)
    birth_date = models.DateField(null = True,blank=True)
    first_deposit_date = models.DateField(auto_now_add=True)
    balance = models.DecimalField(default=0,max_digits=12,decimal_places=2)
    
    def __str__(self):
        return str(self.account_no)
    
class UserAdress(models.Model):
    user = models.OneToOneField(User,related_name='address',on_delete=models.CASCADE)
    
    street_address = models.CharField(max_length=100)
    postal_code = models.IntegerField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    
    def __str__(self):
        return self.user.username