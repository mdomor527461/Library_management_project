from django.db import models
from category.models import CategoryModel
from django.contrib.auth.models import User
# Create your models here.
class BookModel(models.Model):
    img = models.ImageField(upload_to='images/')
    title = models.CharField(max_length=255)
    borrowing_price = models.IntegerField()
    description = models.TextField()
    category = models.ForeignKey(CategoryModel,on_delete = models.CASCADE)
    
    def __str__(self) -> str:
        return self.title
    

class BorrowingModel(models.Model):
    book_id = models.IntegerField()
    borrow_date = models.DateTimeField(auto_now_add=True,null=True)
    
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name='book')
    def __str__(self) -> str:
        return f"book id : {self.book_id} user_id : {self.user_id} borrowing date : {self.borrow_date}"


    
    
class ReviewModel(models.Model):
    
    name = models.CharField(max_length=255)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True,null=True)
    
    book = models.ForeignKey( to = BookModel, on_delete=BookModel,related_name='reviews')
    
    
    