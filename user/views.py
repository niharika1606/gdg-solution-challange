from django.shortcuts import render,redirect,HttpResponse
from rest_framework.response import Response
from rest_framework import status
from django.contrib import messages
from .forms import UserRegistrationForm,UserUpdateForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import uuid
from django.contrib.auth.models import User
def registeruser(request):
    return render(request,'user/register.html')
# Create your views here.
def register(request):
    if request.method=='POST':
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            form.save()
            messages.success(request,f'Account created Successfully!\nYou can to LogIn Now')
            return redirect('login')
        else:
            # If the form is invalid, render the same page with form errors
            messages.success(request,f'try again!')    
            return render(request, 'user/register.html', {'form': form})
    else:
     form=UserRegistrationForm()
     return render(request,'user/register.html',{'form':form})
@login_required
def custom_logout(request):
    logout(request)  # Log the user out
    return render(request, 'user/logout.html') 

@login_required
def Profile(request):
    
    if request.method=='POST':
     u_form=UserUpdateForm(request.POST,instance=request.user)
     p_form=ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
     if u_form.is_valid() and p_form.is_valid():
      u_form.save()
      p_form.save() 
      messages.success(request,f'Account Updated Successfully!\n')
      return redirect('profile')
    else:
     u_form=UserUpdateForm(instance=request.user)
     p_form=ProfileUpdateForm(instance=request.user.profile)
    context={
        'u_form':u_form,
        'p_form':p_form
    }
    return render(request,'user/profile.html',context)
