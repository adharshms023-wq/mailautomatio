from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Recipient, EmailTemplate, EmailLog

admin.site.register(Recipient)
admin.site.register(EmailTemplate)
admin.site.register(EmailLog)