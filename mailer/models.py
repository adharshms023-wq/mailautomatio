from django.db import models

# Create your models here.
from django.db import models

class Recipient(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class EmailTemplate(models.Model):
    title = models.CharField(max_length=100)
    subject = models.CharField(max_length=200)
    body = models.TextField()

    def __str__(self):
        return self.title


class EmailLog(models.Model):
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.recipient.name} - {self.subject}"