from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import TemplateView,UpdateView,DetailView,FormView,CreateView
from books.models import BookModel,CategoryModel
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from . import forms
from books import models
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.mail import EmailMessage,EmailMultiAlternatives
from django.template.loader import render_to_string
import datetime
from books.forms import ReviewForm

#sending email 
names = []
bodies = []
def transaction_email(user,subject,amount,template):
    message = render_to_string(template,{
        'user':user,
        'amount' : amount
    })
    send_email = EmailMultiAlternatives(subject,'',to=[user.email])
    send_email.attach_alternative(message,'text/html')
    send_email.send()

# Create your views here.
def home(request,slug=None):
    data =BookModel.objects.all()
    
    if slug is not None: 
        category = CategoryModel.objects.get(slug = slug)   
        data = BookModel.objects.filter(category = category) 
    categories = CategoryModel.objects.all() 
    return render(request, 'base.html', {'data' : data, 'categories':categories})

@login_required
def profile(request):
    borrow = models.BorrowingModel.objects.filter(user = request.user)
    books = []
    for id in borrow:
        books.append(models.BookModel.objects.get(pk = id.book_id))
    return render(request,'profile.html',{'books' : books,'borrows' : borrow})

method_decorator(login_required,name='dispatch')
class Update_profile(UpdateView):
    model = User
    template_name = 'update_profile.html'
    form_class = forms.UpdateProfileForm
    success_url = reverse_lazy('profile')
    
    def get_object(self,queryset = None):
        return self.request.user
    
    def form_valid(self,form):
        messages.success(self.request,"profile updated successfully")
        return super().form_valid(form)

@method_decorator(login_required,name='dispatch')
class Book_Details(DetailView):
    model = models.BookModel
    template_name = 'book_details.html'
    context_object_name = 'book'
    
    
@method_decorator(login_required,name='dispatch')
class DipositeView(CreateView):
    form_class = forms.DepositeForm
    template_name = 'deposite.html'
    success_url = reverse_lazy('homepage')
    
    def form_valid(self,form):
        amount = form.cleaned_data['amount']
        account = self.request.user.account
        account.balance += amount
        account.save(
            update_fields = ['balance']
        )
        
        transaction_email(self.request.user,"deposite mail",amount,'deposite_mail.html')
        messages.success(self.request,f"{amount} diposite successfully")
        return super().form_valid(form)
    
@login_required
def borrowing(request,id):
    book = models.BookModel.objects.get(pk = id)
    
    if book.borrowing_price <= request.user.account.balance:
        request.user.account.balance -= book.borrowing_price
        borrow = models.BorrowingModel(book_id = id,user = request.user,borrow_date = datetime.datetime.now())
        request.user.account.save(
            update_fields = ['balance']
        )
        borrow.save()
        transaction_email(request.user,"Borrowing mail",book.borrowing_price,"borrowing.html")
        messages.success(request,f"{book.title} book borrowed successfully")
    else:
        messages.warning(request,"you have not enough money to borrow this book")
    return redirect('profile')

@login_required
def return_book(request,id):
    # book = models.BookModel.objects.filter(id = )
    # print(book)
   
    borrow = models.BorrowingModel.objects.get(pk = id)
    book = models.BookModel.objects.get(pk = borrow.book_id)
    request.user.account.balance += book.borrowing_price
    request.user.account.save(
        update_fields = ['balance']
    )
    print(borrow)
    borrow.delete()
    transaction_email(request.user,"return book",request.user.account.balance,"return.html")
    messages.success(request,f" return {book.title} successfully" )
    return redirect('profile')

@login_required
def add_review(request, book_id):
    book = get_object_or_404(models.BookModel, pk=book_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            name = form.cleaned_data.get('name')
            body = form.cleaned_data.get('body')
            names.append(name)
            bodies.append(body)
            review.book = book
            review.save()
            messages.success(request,"review add successfully")
            # Redirect or render success response
            return render(request,"show_review.html",{'names':names,'bodies':bodies})
    else:
        form = ReviewForm()
    return render(request, 'add_review.html', {'form': form})

def show_review(request):
    return render(request,'show_review.html',{'names' : names, 'bodies' : bodies})