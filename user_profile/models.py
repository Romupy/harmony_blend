from django.db import models
from django.utils import timezone
import uuid


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, null=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    presentation = models.TextField(null=True)
    registration_date = models.DateTimeField(default=timezone.now,
                                             verbose_name="Date d'inscription")

    class Meta:
        verbose_name = "profile"
        ordering = ['registration_date']

    def __str__(self):
        return f"Profil de {self.first_name}"
