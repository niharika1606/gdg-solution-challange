from django.shortcuts import render,redirect,HttpResponse
from rest_framework.response import Response
from rest_framework import status
from django.contrib import messages
from .forms import UserRegistrationForm,UserUpdateForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import uuid
from django.contrib.auth.models import User
from .models import Profile 
def registeruser(request):
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
    return render(request, 'uploads/home.html') 

@login_required
def profile_view(request):
    # Retrieve the current user's profile
    profile = Profile.objects.get(user=request.user)
    
    # Pass the profile to the template
    context = {
        'profile': profile
    }
    return render(request, 'user/profile.html', context)
