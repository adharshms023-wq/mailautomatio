from groq import Groq
from django.conf import settings


client = Groq(api_key=settings.GROQ_API_KEY)


def generate_ai_email(idea, tone):

    response = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a professional email marketing expert."
            },
            {
                "role": "user",
                "content": f"""
Create a professional email.

Idea: {idea}
Tone: {tone}

Return format:
SUBJECT:
HEADLINE:
BODY:
CTA:
"""
            }
        ]
    )

    return response.choices[0].message.content