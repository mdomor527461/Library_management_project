from django.http import HttpResponse
from django.shortcuts import render,redirect
from . import forms
from django.views.generic import FormView,UpdateView
from django.contrib.auth.views import LoginView,LogoutView,PasswordChangeView
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
# Create your views here.

class UserRegistrationView(FormView):
    template_name = 'accounts/user_registration.html'
    form_class = forms.UserRegistrationForm
    def get_success_url(self):
        return reverse_lazy('homepage')
    
    def form_valid(self, form):
        user = form.save()
        login(self.request,user)
        messages.success(self.request,f"welcome {user} registration successfully ")
        return super().form_valid(form)
    
class UserLoginView(LoginView):
    template_name = 'accounts/user_login.html'
    def get_success_url(self):
        messages.success(self.request,f"welcome {self.request.user} login successfully ")
        return reverse_lazy('homepage')
    
@login_required 
def user_logout(request):
    messages.warning(request,"logout successfully")
    logout(request)
    return redirect('login')
    