from django.http import JsonResponse
from django.views import View
from django.shortcuts import render, redirect, reverse
from uploads.models import essay
import google.generativeai as genai
import os
from django.conf import settings
from user.models import Profile
from django.http import JsonResponse
from django.db import transaction
GOOGLE_CLOUD_API_KEY = os.getenv("GOOGLE_CLOUD_API_KEY")

genai.configure(api_key=GOOGLE_CLOUD_API_KEY)
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
)
def GenerateResponse(prompt):
  response = model.generate_content([
  f"input: I am providing you the text essay uploaded by student - {prompt}.Do the stress detection.Suppose you are the mentor of students.State if the user response  user is 😊 Not stressed,😟 Stressed or 😐 neutral.based on the sentiment analysis result of student in only one word, suggest betterment ways for user to stay positive in fun interactive and short act as their real therapist person. add emojis and engagig text keeping the para short you can aslo include trending memes or jokes if user is sad. do everything possible to enhance the mood of student? remember your response is directly being displayed to students",
  "output: ",])

  return (response.text)
class GeminiChatView(View):
    def get(self, request):
        return render(request, 'uploads/chat.html', {'response': ''})

    def post(self, request):
        # Retrieve the prompt from the HTML form input
        prompt = request.POST.get('content', '')
        
        if prompt:
            try:
                # Generate response from the model
                response = GenerateResponse(prompt)

                # Store the result in the database with the current user
                essay.objects.create(
                    title=self.title,
                    content=self.content,
                    student=request.user,    # Store the current user
                    results=response,

                )
            except Exception as e:
                response = f"Error: {str(e)}"
        else:
            response = "Please enter a prompt."

        # Render the same template with the response
        return render(request, 'uploads/chat.html', {'response': response, 'prompt': prompt})
class UpdateProgressView(View):
    """
    This view updates the user's progress after adding a new post.
    It calculates positive, neutral, and negative percentages.
    """
    def post(self, request, *args, **kwargs):
        # Get the current user
        user = request.user

        # Fetch all essays of the current user
        posts = essay.objects.filter(student=user)

        # Initialize counters
        positive = 0
        neutral = 0
        negative = 0

        # Classify each result into sentiment categories
        for post in posts:
            result = post.results.lower()

            if "Not stressed" in result:
                positive += 1
            elif "Stressed" in result:
                negative += 1
            else:
                neutral += 1

        total_posts = posts.count()

        # Avoid division by zero
        if total_posts == 0:
            progress = {
                'positive': 0,
                'neutral': 0,
                'negative': 0,
            }
        else:
            # Calculate percentages
            progress = {
                'positive': round((positive / total_posts) * 100, 2),
                'neutral': round((neutral / total_posts) * 100, 2),
                'negative': round((negative / total_posts) * 100, 2),
            }

        # Update the profile with the new progress
        try:
            with transaction.atomic():  # Ensure atomic update
                profile = Profile.objects.get(user=user)
                profile.positive = progress['positive']
                profile.neutral = progress['neutral']
                profile.negative = progress['negative']
                profile.save()

            return JsonResponse({'status': 'success', 'progress': progress})

        except Profile.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Profile not found'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
