from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import essay
from gemini.views import GenerateResponse  # Import the ML model function

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