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
    context_object_name = 'essays'  # Use a plural name for consistency
    ordering = ['-created_at']  
    paginate_by = 5

    def get_queryset(self):
        if self.request.user.is_superuser:
            # Superuser: Show all essays
            return essay.objects.all()
        else:
            # Regular user: Show only their essays
            return essay.objects.filter(student=self.request.user)

    def get_template_names(self):
        # Return the appropriate template based on the user type
        return ['uploads/home.html'] if self.request.user.is_superuser else ['uploads/essay_list.html']
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
@login_required
def home(request):
 if request.user.is_superuser:
        # Superuser: Show all essays
        posts = essay.objects.all()
        return render(request, 'uploads/home.html', {'post': posts})
 else:
        # Regular user: Show only their essays
        user_content = essay.objects.filter(student=request.user)
        return render(request, 'uploads/essay_list.html', {'user_content': user_content})