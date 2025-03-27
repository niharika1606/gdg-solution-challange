"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from uploads.views import (
    PostListView,
    PostCreateView,
    PostDetailView,

    )
from user import views as user_views
from uploads import views as up_views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from gemini.views import GeminiChatView

urlpatterns = [
    path('admin/', admin.site.urls), 
    path('register/',user_views.registeruser,name='register'),
    path('new/',PostCreateView.as_view(),name='post-create'),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/',user_views.custom_logout,name='logout'),
    path('profile/',user_views.Profile,name='profile'),
    path('list/',PostListView.as_view(),name='list-page'),
    path('',up_views.home,name='home-page'),
    path('about/',up_views.about,name='about'),
     path('chat/', GeminiChatView.as_view(), name='gemini_chat'),
    path('post/<int:pk>/',PostDetailView.as_view(),name='post-detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)