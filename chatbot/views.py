import os
import time

from dotenv import load_dotenv
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from google import genai

load_dotenv()


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
            {"reply": "The AI service is not configured correctly."},
            status=500,
        )

    prompt = (
        "You are a friendly chatbot. Answer clearly and briefly. "
        "Only answer questions about nature and finance. "
        "For unrelated questions, politely explain that you "
        "currently support nature and finance only.\n\n"
        f"User question: {message}"
    )

    try:
        client = genai.Client(
            api_key=api_key,
            http_options={"timeout": 30000},
        )

        for attempt in range(3):
            try:
                response = client.models.generate_content(
                   model="gemini-3.5-flash-lite",
                    contents=prompt,
                )

                reply = response.text or (
                    "Sorry, I couldn't generate a response."
                )

                return JsonResponse({"reply": reply})

            except Exception as error:
                error_message = str(error).upper()

                print(
                    f"Gemini attempt {attempt + 1} failed:",
                    repr(error),
                )

                temporary_error = any(
                    code in error_message
                    for code in (
                        "503",
                        "504",
                        "DEADLINE_EXCEEDED",
                        "UNAVAILABLE",
                        "429",
                        "RESOURCE_EXHAUSTED",
                    )
                )

                if not temporary_error:
                    raise

                if attempt < 2:
                    time.sleep(1 + (2 ** attempt))

        return JsonResponse(
            {
                "reply": (
                    "Gemini is taking too long to respond. "
                    "Please try again shortly."
                )
            },
            status=503,
        )

    except Exception as error:
        print("Gemini API error:", repr(error))

        return JsonResponse(
            {
                "reply": (
                    "The AI service is temporarily unavailable. "
                    "Please try again shortly."
                )
            },
            status=503,
        )