from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'positive', 'neutral', 'negative', 'total_posts')  # Display progress fields
    list_filter = ('user',)  # Add filtering options
    search_fields = ('user__username',) 