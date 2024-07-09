from django.db import models

# Create your models here.
class DepositeModel(models.Model):
    amount = models.IntegerField()
    
