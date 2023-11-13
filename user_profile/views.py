from django.shortcuts import render, get_object_or_404
from django.http import Http404
from user_profile.models import Profile
from .forms import ProfileForm



def read(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    return render(request, 'profile/read.html', locals())


def create(request):
    form = ProfileForm(request.POST or None)
    if form.is_valid():
        form.save()

    return render(request, 'profile/create.html', locals())


def form_create(request):
    form = ProfileForm(request.POST or None)
    if form.is_valid():
        form.save()

    return render(request, 'profile/create.html', locals())
