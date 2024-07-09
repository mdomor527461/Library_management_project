from django.db import models

# Create your models here.
class CategoryModel(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,blank=True,null=True)
    def __str__(self):
        return self.name