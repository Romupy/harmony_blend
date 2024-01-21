import os

import requests
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from PIL import Image
import uuid


class Profile(models.Model):
    MAX_SIZE = (500, 500)
    QUALITY = 40

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(
        upload_to='images/', verbose_name="Photo de profil"
    )
    first_name = models.CharField(max_length=50, verbose_name="Prénom")
    last_name = models.CharField(max_length=50, null=True, verbose_name="Nom")
    presentation = models.TextField(
        null=True, blank=True, verbose_name="Présentation"
    )
    registration_date = models.DateTimeField(
        default=timezone.now, verbose_name="Date d'inscription"
    )
    skin_brightness = models.FloatField(
        null=True, blank=True, verbose_name="Luminosité de la peau"
    )
    skin_info = models.TextField(
        null=True, blank=True, verbose_name="Couleur de peau"
    )

    class Meta:
        verbose_name = "Profil"
        ordering = ['registration_date']

    def __str__(self):
        return f"Profil de {self.first_name} {self.last_name}"

    def check_profile_image(self):
        message = "Image de profil conforme !"
        valid = True
        file_path = os.path.join(settings.MEDIA_ROOT, self.image.name)
        files = {'image': (self.image.name, open(file_path, 'rb'))}
        response = requests.post(
            f'{settings.AI_COMPUTER_VISION_API_URL}/face', files=files
        )
        if response.status_code != 201:
            valid = True
            message = ("Impossible de vérifier l'image de profil, "
                       "artificial_intelligence_computer_vision_api a "
                       "rencontré une erreur !")
            return valid, message
        content = response.json()['analysis_results']
        if content['number_of_faces_detected'] == 1:
            self.skin_brightness = content['facial_skin'][0]['skin_brightness']
            self.skin_info = content['facial_skin'][0]['skin_info']
            self.save()
        elif content['number_of_faces_detected'] == 0:
            valid = False
            message = "Image de profil non conforme: aucun visage détecté !"
            os.remove(file_path)
            self.delete()
        elif content['number_of_faces_detected'] > 1:
            valid = False
            message = ("Image de profil non conforme: plusieurs visages "
                       "détectés !")
            os.remove(file_path)
            self.delete()
        return valid, message

    @receiver(post_save, sender='user_profile.Profile')
    def compress_image_before_save(sender, instance, **kwargs):
        """
        Compress and resize the image before saving it

        Keyword arguments:
        sender -- (django.db.models.Model) The model class
        instance -- (django.db.models.Model) The actual instance being saved
        """
        if (hasattr(instance, 'image')
                and instance.image and instance.image.file):
            sender.compress_and_resize_image(instance.image)

    @staticmethod
    def compress_and_resize_image(image):
        """
        Compress and resize the image

        Keyword arguments:
        image -- (django.db.models.ImageField) The image to compress and resize
        """
        with Image.open(image) as img:
            if img.mode == 'RGBA':
                img = img.convert('RGB')
            img.thumbnail(Profile.MAX_SIZE)
            file_path = os.path.join(settings.MEDIA_ROOT + "/" + image.name)
            img.save(file_path, "JPEG", quality=Profile.QUALITY)
