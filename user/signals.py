from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
from uploads.models import essay

# Automatically create a profile for every new user
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# Automatically save the profile whenever the user is saved
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

@receiver(post_save, sender=essay)
def update_profile_progress(sender, instance, created, **kwargs):
    print("Signal Triggered")  # ✅ Check if the signal is firing
    
    if created:
        print(f"Updating profile for: {instance.student.username}")

        # Fetch or create profile
        profile, created = Profile.objects.get_or_create(user=instance.student)

        # Get all essays for the user
        posts = essay.objects.filter(student=instance.student)

        # Initialize counters
        positive = sum(1 for post in posts if "not stressed" in post.results.lower())
        neutral = sum(1 for post in posts if "neutral" in post.results.lower())
        negative = sum(1 for post in posts if "stressed" in post.results.lower())

        total_posts = posts.count()

        # Calculate percentages safely
        profile.positive = round((positive / total_posts) * 100, 2) if total_posts > 0 else 0
        profile.neutral = round((neutral / total_posts) * 100, 2) if total_posts > 0 else 0
        profile.negative = round((negative / total_posts) * 100, 2) if total_posts > 0 else 0

        profile.save()
        print(f"Profile updated: {profile.positive}% Positive, {profile.neutral}% Neutral, {profile.negative}% Negative")