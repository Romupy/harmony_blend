from django.db import models
from django.utils import timezone


class Profile(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, null=True)
    presentation = models.TextField(null=True)
    registration_date = models.DateTimeField(default=timezone.now,
                                             verbose_name="Date d'inscription")

    class Meta:
        verbose_name = "profile"
        ordering = ['registration_date']

    def __str__(self):
        return f"Profil de {self.first_name}"
