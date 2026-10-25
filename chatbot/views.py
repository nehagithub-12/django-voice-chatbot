
import os
from dotenv import load_dotenv

load_dotenv()

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from google import genai


def chatbot_home(request):
    return render(request, "chatbot/index.html")


@csrf_exempt
def chat_response(request):
    if request.method != "POST":
        return JsonResponse(
            {"reply": "Please send a message using the chat box."},
            status=405,
        )

    message = request.POST.get("message", "").strip()

    if not message:
        return JsonResponse(
            {"reply": "Please type a message first."},
            status=400,
        )

    api_key = os.getenv("GEMINI_API_KEY", "").strip()

    if not api_key:
        print("ERROR: Gemini API key was not loaded.")
        return JsonResponse(
            {"reply": "API key missing. Please check your .env file."},
            status=500,
        )

    try:
        client = genai.Client(api_key=api_key)

        prompt = (
            "You are a friendly chatbot. Answer clearly and briefly. "
            "Only answer questions about nature and finance. "
            "For unrelated questions, politely explain that you "
            "currently support nature and finance only.\n\n"
            f"User question: {message}"
        )

        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt,
        )

        reply = response.text or "Sorry, I couldn't generate a response."

        return JsonResponse({"reply": reply})

    except Exception as error:
        print("Gemini API error:", repr(error))
        return JsonResponse(
            {"reply": "The AI service failed. Check the VS Code terminal."},
            status=500,
        )
