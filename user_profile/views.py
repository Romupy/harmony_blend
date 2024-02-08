from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from user_profile.models import UserProfile
from .forms import UserProfileUpdateForm


@login_required
def read_user_profile(request, user_profile_id):
    """
    View to read a user_profile

    Keyword arguments:
    request -- (django.http.HttpRequest) The HttpRequest object containing all
    information about HTTP request.
    profile_id -- (str) The user_profile id

    Returns:
    django.http.HttpResponse -- An HttpResponse object representing the view
    response
    """
    user_profile = get_object_or_404(UserProfile, id=user_profile_id)
    return render(request, 'user_profile/read.html', locals())


@login_required
def list_user_profiles(request):
    """
    View to list profiles

    Keyword arguments:
    request -- (django.http.HttpRequest) The HttpRequest object containing all
    information about HTTP request.

    Returns:
    django.http.HttpResponse -- An HttpResponse object representing the view
    response
    """
    user_profiles = UserProfile.objects.all()
    return render(request, 'user_profile/list.html', locals())


@login_required
def update_user_profile(request, user_profile_id):
    """
    View to update a user_profile

    Keyword arguments:
    request -- (django.http.HttpRequest) The HttpRequest object containing all
    information about HTTP request.
    profile_id -- (str) The user_profile id

    Returns:
    django.http.HttpResponse -- An HttpResponse object representing the view
    response
    """
    user_profile = get_object_or_404(UserProfile, id=user_profile_id)
    form = UserProfileUpdateForm(
        request.POST or None, request.FILES or None, instance=user_profile
    )
    if form.is_valid():
        user_profile = form.save()
        valid, message = user_profile.check_profile_image()
        if not valid:
            messages.error(request, message)
            return render(request, 'user_profile/update.html', locals())
        return redirect('read_user_profile', user_profile_id=user_profile.id)
    else:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(
                    request,
                    f"Erreur dans le champ <<{field}>> : {error}"
                )
    return render(request, 'user_profile/update.html', locals())


@login_required
def delete_user_profile(request, user_profile_id):
    """
    View to delete a user_profile

    Keyword arguments:
    request -- (django.http.HttpRequest) The HttpRequest object containing all
    information about HTTP request.

    Returns:
    django.http.HttpResponse -- An HttpResponse object representing the view
    response
    """
    user_profile = get_object_or_404(UserProfile, id=user_profile_id)
    if request.method == 'POST':
        user_profile.delete()
        return redirect('list_profiles')
    return render(request, 'user_profile/delete.html', locals())
