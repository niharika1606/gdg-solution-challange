from django.http import JsonResponse
from django.views import View
from django.shortcuts import render, redirect
import google.generativeai as genai
import os
genai.configure(api_key=os.getenv('GOOGLE_CLOUD_API_KEY'))

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
  f"input: {prompt}",
  "output: ",
])

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
            except Exception as e:
                response = f"Error: {str(e)}"
        else:
            response = "Please enter a prompt."

        # Render the same template with the response
        return render(request, 'uploads/chat.html', {'response': response, 'prompt': prompt})