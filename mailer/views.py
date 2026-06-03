from django.shortcuts import render
from django.core.mail import send_mail
import csv

EMAIL_TEMPLATES = {
    "welcome": {
        "subject": "Welcome to Our System 🎉",
        "message": "Hello! Welcome to our Email Automation System. We are happy to have you."
    },
    "offer": {
        "subject": "Special Offer 🔥",
        "message": "Limited time offer! Get 50% discount today only."
    },
    "update": {
        "subject": "System Update 📢",
        "message": "We have updated our system with new features."
    }
}
from django.http import JsonResponse

progress_data = {"progress": 0}

def progress(request):
    return JsonResponse(progress_data)

def home(request):
    template_data = None

    if request.method == "POST":
        template_key = request.POST.get("template")

        subject = request.POST.get("subject")
        message = request.POST.get("message")

        # If template selected, override message
        if template_key in EMAIL_TEMPLATES:
            subject = EMAIL_TEMPLATES[template_key]["subject"]
            message = EMAIL_TEMPLATES[template_key]["message"]

        csv_file = request.FILES.get("file")
        if csv_file:
            file_data = csv_file.read().decode("utf-8").splitlines()
            reader = csv.reader(file_data)
            emails = [row[0] for row in reader if row]

            for email in emails:
                send_mail(
                    subject,
                    message,
                    "yourgmail@gmail.com",
                    [email],
                )

        return render(request, "home.html", {
            "message": "Emails Sent ✔",
            "templates": EMAIL_TEMPLATES
        })

    return render(request, "home.html", {
        "templates": EMAIL_TEMPLATES
    })