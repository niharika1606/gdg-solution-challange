from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import essay
from gemini.views import GenerateResponse  # Import the ML model function
from user.models import Profile
from django.db import transaction
@receiver(post_save, sender=essay)
def run_ml_model(sender, instance, created, **kwargs):
    """
    Automatically run the ML model when a new essay is added.
    """
    if created:  # Only run on new essay creation
        try:
            # Run the ML model on the essay content
            result = GenerateResponse(instance.content)
            
            # Save the ML-generated result into the essay
            instance.results = result
            instance.save()

        except Exception as e:
            instance.results = f"Error: {str(e)}"
            instance.save()


@receiver(post_save, sender=essay)
def update_progress_on_save(sender, instance, **kwargs):
    """
    Signal handler to automatically update profile progress
    when a new essay is saved.
    """
    user = instance.student

    try:
        # ✅ Fetch all essays of the current user
        posts = essay.objects.filter(student=user)

        # Initialize counters
        positive = 0
        neutral = 0
        negative = 0

        # Classify each result into sentiment categories
        for post in posts:
            result = post.results.lower()

            # ✅ Match actual sentiment labels from the generated content
            if "😊" in result or "not stressed" in result:
                positive += 1
            elif "😟" in result or "stressed" in result:
                negative += 1
            else:
                neutral += 1

        total_posts = posts.count()

        # ✅ Calculate percentages
        if total_posts > 0:
            progress = {
                'positive': round((positive / total_posts) * 100, 2),
                'neutral': round((neutral / total_posts) * 100, 2),
                'negative': round((negative / total_posts) * 100, 2),
            }
        else:
            progress = {'positive': 0, 'neutral': 0, 'negative': 0}

        # ✅ Update the user's profile with the new progress
        with transaction.atomic():
            profile, created = Profile.objects.get_or_create(user=user)
            profile.positive = progress['positive']
            profile.neutral = progress['neutral']
            profile.negative = progress['negative']
            profile.save()

        print(f"✅ Profile updated: {progress}")

    except Exception as e:
        print(f"❌ Error updating profile progress: {str(e)}")