from django.http import JsonResponse
from django.views import View
from django.shortcuts import render, redirect
from uploads.models import essay
import google.generativeai as genai
from transformers import pipeline
import os
genai.configure(api_key=os.getenv('GOOGLE_CLOUD_API_KEY'))
classifier = pipeline('text-classification', model='distilbert-base-uncased-finetuned-sst-2-english')
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
  res =classifier(prompt)
  response = model.generate_content([
  f"input: Suppose you are the mentor of students. We {res} suggest betterment ways for user to stay positive?",
  "output: ",])

  return (response.text)
class GeminiChatView(View):
    def get(self, request):
        return render(request, 'uploads/chat.html', {'response': ''})

    def post(self, request):
        # Retrieve the prompt from the HTML form input
        prompt = request.POST.get('prompt', '')
        
        if prompt:
            try:
                # Generate response from the model
                response = GenerateResponse(prompt)

                # Store the result in the database with the current user
                essay.objects.create(
                    title="results check",
                    content="checking purposes",
                    student=request.user,    # Store the current user
                    results=response,

                )
            except Exception as e:
                response = f"Error: {str(e)}"
        else:
            response = "Please enter a prompt."

        # Render the same template with the response
        return render(request, 'uploads/chat.html', {'response': response, 'prompt': prompt})