from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import essay
# Create your views here.
class PostListView(ListView):
    model=essay
    template_name='home.html'
    context_object_name='post'
    ordering='created_at'
    paginate_by=5

class PostDetailView(DetailView):
    model=essay
    template_name='fashion/post_detail.html'
class PostCreateView(LoginRequiredMixin,CreateView):
    model=essay
    template_name='post_form.html'
    fields=['collection','type','price_Range']
    def form_valid(self,form):
        form.instance.designed_by=self.request.user
        return super().form_valid(form)
def home(request):
    context={
        'post':essay.objects.all()
    }
    return render(request,'uploads/home.html',context)