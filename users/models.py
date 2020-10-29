from django.db import models

class EmailVerification(models.Model):
    email = models.CharField(max_length=256)
    OTP = models.IntegerField()
    username = models.CharField(max_length=256)
    purpose = models.CharField(max_length=100)
    def __str__(self):
        return self.email
