from django.shortcuts import render, redirect
from django.urls import reverse  
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import essay
from django.urls import reverse_lazy
from gemini.views import GenerateResponse
from user.models import Profile
from django.views import View
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
class PostListView(LoginRequiredMixin,ListView):
    model = essay  
    template_name = 'uploads/essay_list.html'  
    context_object_name = 'essays'  
    ordering = ['-created_at']  
    def get_queryset(self):
            return essay.objects.filter(student=self.request.user)

class PostDetailView(DetailView):
    model = essay
    template_name = 'uploads/post_detail.html'

class PostCreateView(LoginRequiredMixin, CreateView):
    """
    View to create a new essay and automatically run the ML model.
    """
    model = essay
    template_name = 'uploads/post_form.html'
    fields = ['title', 'content']  # Fields in the form

    def form_valid(self, form):
        """
        Run ML model on the content after saving the essay.
        """
        # Associate the essay with the current user
        form.instance.student = self.request.user  
        
        # Save the form (create the essay object)
        response = super().form_valid(form)
        
        # Run the ML model and save the results
        try:
            result = GenerateResponse(form.instance.content)
            form.instance.results = result  # Save ML result in the essay
            form.instance.save()

            messages.success(self.request, "Done! Your words are out there. Keep up the great work!")

        except Exception as e:
            form.instance.results = f"Error: {str(e)}"
            form.instance.save()
            messages.error(self.request, f"Error generating ML result: {str(e)}")

        return response

    
    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.pk})

class PostDetailView(DetailView):
    model=essay
    template_name='uploads/post_detail.html'
    
def home(request):
    return render(request, "uploads/home.html")

def about(request):
    return render(request, "uploads/about.html")
def superuser_dashboard(request):
    profiles = Profile.objects.all()

    total_positive = sum(profile.positive for profile in profiles)
    total_negative = sum(profile.negative for profile in profiles)
    
    total_neutral = sum(profile.neutral for profile in profiles)

    # Calculate progress percentage
    total_score = total_positive + total_negative
    progress_percentage = (total_positive / total_score) * 100 if total_score > 0 else 0

    context = {
        'profiles': profiles,
        'total_positive': total_positive,
        'total_negative': total_negative,
        'total_neutral': total_neutral,
    }

    return render(request, 'uploads/dashboard.html', context)
