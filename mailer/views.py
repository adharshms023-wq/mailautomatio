from django.core.mail import send_mail
from django.http import HttpResponse

 
def home(request):
    return HttpResponse("Email Automation System Running")

def send_test_email(request):
    send_mail(
        "Test Subject",
        "Hello from Django",
        "from@example.com",
        ["to@example.com"],
    )
    return HttpResponse("Email Sent")