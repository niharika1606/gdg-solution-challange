from django.shortcuts import render, redirect
from django.urls import reverse  
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import essay
from django.urls import reverse_lazy
class PostListView(LoginRequiredMixin,ListView):
    model = essay  
    template_name = 'uploads/essay_list.html'  
    context_object_name = 'essays'  
    ordering = ['-created_at']  
    paginate_by = 5
    def get_queryset(self):
        if self.request.user.is_superuser:
            return essay.objects.all()
        else:
            return essay.objects.filter(student=self.request.user)

class PostDetailView(DetailView):
    model = essay
    template_name = 'uploads/post_detail.html'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = essay 
    template_name = 'uploads/post_form.html'
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.student = self.request.user  
        messages.success(self.request, "Post created successfully!")
        return super().form_valid(form)

  
    def get_success_url(self):
        return reverse_lazy('home-page') 

class PostDetailView(DetailView):
    model=essay
    template_name='uploads/post_detail.html'
    
def home(request):
    return render(request, "uploads/home.html")

def about(request):
    return render(request, "uploads/about.html")