import os

from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from user_profile.models import Profile
from .forms import ProfileForm


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
        profile = form.save()
        valid, message = profile.check_profile_image()
        if not valid:
            return render(request, 'profile/create.html', locals())
        return redirect('profile_read', profile_id=profile.pk)
    return render(request, 'profile/create.html', locals())


def form_create(request):
    form = ProfileForm(request.POST or None)
    if form.is_valid():
        form.save()

    return render(request, 'profile/create.html', locals())
