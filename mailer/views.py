from django.shortcuts import render
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from groq import Groq


# ---------------- GROQ SETUP ----------------
client = Groq(api_key=settings.GROQ_API_KEY)


def generate_ai_email(idea, tone):

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {
                "role": "system",
                "content": "You are an expert email marketing assistant."
            },
            {
                "role": "user",
                "content": f"""
Create a professional email.

Idea: {idea}
Tone: {tone}

Return:
SUBJECT:
HEADLINE:
BODY:
CTA:
"""
            }
        ]
    )

    return response.choices[0].message.content

# ---------------- HTML TEMPLATE ----------------
def build_template(subject, content, style="startup"):

    if style == "event":
        color = "#f59e0b"
        title = "🎉 Invitation"
    elif style == "corporate":
        color = "#374151"
        title = "Company Update"
    else:
        color = "#2563eb"
        title = "🚀 Announcement"

    return f"""
    <html>
    <body style="font-family:Arial;background:#f4f6f9;padding:30px;">
        <div style="max-width:600px;margin:auto;background:white;padding:30px;border-radius:10px;">

            <h1 style="color:{color};">{title}</h1>
            <h2>{subject}</h2>

            <p style="font-size:16px;line-height:1.8;">
                {content}
            </p>

            <a href="#"
                style="
                display:inline-block;
                margin-top:20px;
                background:{color};
                color:white;
                padding:12px 24px;
                text-decoration:none;
                border-radius:6px;">
                Open
            </a>

        </div>
    </body>
    </html>
    """


# ---------------- MAIN VIEW ----------------
def home(request):

    preview = ""
    ai_output = ""

    if request.method == "POST":

        action = request.POST.get("action")
        idea = request.POST.get("content")
        tone = request.POST.get("tone")
        style = request.POST.get("style")
        subject_manual = request.POST.get("subject")
        emails_text = request.POST.get("emails", "")

        emails = [
            e.strip()
            for e in emails_text.replace(",", "\n").splitlines()
            if e.strip()
        ]

        # ---------------- GENERATE ----------------
        if action == "generate":

            ai_output = generate_ai_email(idea, tone)

            lines = ai_output.split("\n")

            subject = ""
            body = ""

            for line in lines:
                if "SUBJECT:" in line:
                    subject = line.replace("SUBJECT:", "").strip()
                else:
                    body += line + "\n"

            preview = build_template(subject, body, style)

        # ---------------- SEND ----------------
        elif action == "send":

            subject = subject_manual or "No Subject"
            content = idea

            html = build_template(subject, content, style)
            preview = html

            count = 0

            for email in emails:
                try:
                    msg = EmailMultiAlternatives(
                        subject,
                        content,
                        "yourgmail@gmail.com",
                        [email],
                    )
                    msg.attach_alternative(html, "text/html")
                    msg.send()
                    count += 1
                except:
                    pass

            preview += f"<p style='color:green;'>Sent {count} emails</p>"

    return render(request, "home.html", {
        "preview": preview,
        "ai_output": ai_output,
    })