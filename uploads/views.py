from django.shortcuts import render, redirect
from django.urls import reverse  
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import essay
from django.contrib.auth.decorators import login_required
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
    # Always include both querysets in the context
    context = {
        'post': essay.objects.all() if request.user.is_superuser else None,
        'user_content': essay.objects.filter(student=request.user)
    }
    
    # Print the querysets to confirm they are being fetched correctly
    print("Post:", context['post'])
    print("User Content:", context['user_content'])

    return render(request, 'uploads/home.html', context)

    return render(request, 'uploads/home.html', context)