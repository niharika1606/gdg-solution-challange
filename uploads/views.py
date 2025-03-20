from django.shortcuts import render, redirect
from django.urls import reverse  
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import essay
class PostListView(ListView):
    model = essay
    template_name = 'uploads/home.html' 
    context_object_name = 'post'
    ordering = ['-created_at']  
    paginate_by = 5
class PostDetailView(DetailView):
    model = essay
    template_name = 'uploads/post_detail.html'
class PostCreateView(LoginRequiredMixin, CreateView):
    model = essay
    template_name = 'uploads/post_form.html'
    fields = ['title', 'content']

    def get_success_url(self):
        return reverse('home')  

    def form_valid(self, form):
        form.instance.student = self.request.user
        messages.success(self.request, "Post created successfully!")
        return super().form_valid(form)
def home(request):
    context = {
        'post': essay.objects.all()
    }
    return render(request, 'uploads/home.html', context)
