import os

from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from user_profile.models import Profile
from .forms import ProfileForm, ProfileUpdateForm


def create_profile(request):
    """
    View to create a profile

    Keyword arguments:
    request -- (django.http.HttpRequest) The HttpRequest object containing all
    information about HTTP request.

    Returns:
    django.http.HttpResponse -- An HttpResponse object representing the view
    response
    """

    form = ProfileForm(request.POST, request.FILES)
    if form.is_valid():
        uploaded_file = form.cleaned_data['image']
        file_path = os.path.join(
            settings.MEDIA_ROOT + '/images/', uploaded_file.name
        )
        profile = form.save()
        valid, message = profile.check_profile_image()
        if not valid:
            return render(request, 'profile/create_or_update.html', locals())
        return redirect('read_profile', profile_id=profile.pk)
    return render(request, 'profile/create_or_update.html', locals())


def read_profile(request, profile_id):
    """
    View to read a profile

    Keyword arguments:
    request -- (django.http.HttpRequest) The HttpRequest object containing all
    information about HTTP request.
    profile_id -- (str) The profile id

    Returns:
    django.http.HttpResponse -- An HttpResponse object representing the view
    response
    """
    profile = get_object_or_404(Profile, id=profile_id)
    return render(request, 'profile/read.html', locals())


def list_profiles(request):
    """
    View to list profiles

    Keyword arguments:
    request -- (django.http.HttpRequest) The HttpRequest object containing all
    information about HTTP request.

    Returns:
    django.http.HttpResponse -- An HttpResponse object representing the view
    response
    """
    profiles = Profile.objects.all()
    return render(request, 'profile/list.html', locals())


def update_profile(request, profile_id):
    """
    View to update a profile

    Keyword arguments:
    request -- (django.http.HttpRequest) The HttpRequest object containing all
    information about HTTP request.
    profile_id -- (str) The profile id

    Returns:
    django.http.HttpResponse -- An HttpResponse object representing the view
    response
    """
    profile = get_object_or_404(Profile, id=profile_id)
    form = ProfileUpdateForm(
        request.POST or None, request.FILES or None, instance=profile
    )
    if form.is_valid():
        uploaded_file = form.cleaned_data['image']
        file_path = os.path.join(
            settings.MEDIA_ROOT + '/images/', uploaded_file.name
        )
        profile = form.save()
        valid, message = profile.check_profile_image()
        if not valid:
            return render(request, 'profile/create_or_update.html', locals())
        return redirect('read_profile', profile_id=profile.pk)
    return render(request, 'profile/create_or_update.html', locals())


def delete_profile(request, profile_id):
    """
    View to delete a profile

    Keyword arguments:
    request -- (django.http.HttpRequest) The HttpRequest object containing all
    information about HTTP request.

    Returns:
    django.http.HttpResponse -- An HttpResponse object representing the view
    response
    """
    profile = get_object_or_404(Profile, id=profile_id)
    if request.method == 'POST':
        profile.delete()
        return redirect('list_profiles')
    return render(request, 'profile/delete.html', locals())
