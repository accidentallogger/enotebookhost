from django.db import models
from django.conf import settings


class Invite(models.Model):
    email = models.EmailField(unique=True)
    supervisor = models.CharField(max_length=255)
    token = models.CharField(max_length=255)
    uid = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20, default="Pending"
    )  # 'Pending' or 'Accepted'
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
