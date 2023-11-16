import os

from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from user_profile.models import Profile
from .forms import ProfileForm
import requests


def read(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    return render(request, 'profile/read.html', locals())


def create(request):
    form = ProfileForm(request.POST, request.FILES)
    if form.is_valid():
        uploaded_file = form.cleaned_data['image']
        file_path = os.path.join(
            settings.MEDIA_ROOT + '/images/', uploaded_file.name
        )
        instance = form.save()
        files = {'image': (uploaded_file.name, open(file_path, 'rb'))}
        response = requests.post(
            'http://127.0.0.1:8000/image_analysis/face', files=files
        )
        content = response.json()
        if 0 < content['analysis_results']['Number_of_faces_detected'] < 2:
            return render(request, 'profile/create.html', locals())
        else:
            file_path = os.path.join(
                settings.MEDIA_ROOT + '/images/', uploaded_file.name
            )
            os.remove(file_path)
            instance.delete()
        return render(request, 'profile/create.html', locals())


def form_create(request):
    form = ProfileForm(request.POST or None)
    if form.is_valid():
        form.save()

    return render(request, 'profile/create.html', locals())
