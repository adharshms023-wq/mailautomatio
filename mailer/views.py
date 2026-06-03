from django.shortcuts import render
from django.core.mail import EmailMultiAlternatives
import csv

def build_email_html(message):
    return f"""
    <html>
        <body style="font-family:Arial;background:#f4f6f9;padding:20px;">
            <div style="max-width:600px;margin:auto;background:white;padding:20px;border-radius:10px;">
                
                <h2 style="color:#2c3e50;text-align:center;">
                    📧 Email Automation System
                </h2>

                <hr>

                <p style="font-size:16px;line-height:1.6;">
                    {message}
                </p>

                <hr>

                <p style="text-align:center;color:gray;font-size:12px;">
                    Sent via Django Mail System 🚀
                </p>

            </div>
        </body>
    </html>
    """

def home(request):
    preview_html = ""
    message = ""

    if request.method == "POST":
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        csv_file = request.FILES.get("file")

        html_content = build_email_html(message)
        preview_html = html_content

        if csv_file:
            file_data = csv_file.read().decode("utf-8").splitlines()
            reader = csv.reader(file_data)
            emails = [row[0] for row in reader if row]

            for email in emails:
                email_msg = EmailMultiAlternatives(
                    subject,
                    message,
                    "yourgmail@gmail.com",
                    [email],
                )
                email_msg.attach_alternative(html_content, "text/html")
                email_msg.send()

        return render(request, "home.html", {
            "message": "Emails Sent ✔",
            "preview": preview_html
        })

    return render(request, "home.html", {
        "preview": preview_html
    })