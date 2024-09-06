# myapp/models.py

from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age_verified = models.BooleanField(default=False)
# myapp/models.py

from django.db import models
from django.contrib.auth.models import User

class VerificationRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
