from django.contrib import admin
from .models import EmailVerification

class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'username', 'OTP', 'purpose']

admin.site.register(EmailVerification, EmailVerificationAdmin)
