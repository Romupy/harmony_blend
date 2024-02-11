from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from authentication.forms import LoginForm, RegisterForm
from authentication.models import User


def register(request):
    if request.user.is_authenticated:
        logout(request)
        messages.error(request, "Vous avez été déconnecté.")
    is_register = True
    form = RegisterForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            password_confirmation = form.cleaned_data['password_confirmation']
            if password != password_confirmation:
                messages.error(
                    request,
                    f"Erreur dans les champs <<Password>> et "
                    f"<<Password confirmation>>: Les deux mots de passe ne "
                    f"sont pas identiques."
                )
                return render(
                    request, 'authentication/register.html', locals()
                )

            user = User.objects.create_user(email, email, password)
            user.user_profile.first_name = form.cleaned_data['first_name']
            user.user_profile.last_name = form.cleaned_data['last_name']
            user.user_profile.save()
            messages.success(request, "Inscription réussie")
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
            return redirect('update_user_profile')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(
                        request,
                        f"Erreur dans le champ <<{field}>> : {error}"
                    )
    return render(request, 'authentication/register.html', locals())


def connection(request):
    if request.user.is_authenticated:
        messages.error(request, "Vous êtes déjà connecté !")
        return redirect(
            'read_user_profile', user_profile_id=request.user.user_profile.id
        )
    form = LoginForm(request.POST or None)
    if form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data['email'],
            password=form.cleaned_data['password']
        )
        if user is not None:
            login(request, user)
            return redirect(
                'read_user_profile', user_profile_id=user.user_profile.id
            )
        else:
            messages.error(
                request, "Erreur lors de la tentative de connexion"
            )
            return redirect('connection')
    return render(request, 'authentication/connection.html', locals())


@login_required
def log_off(request):
    logout(request)
    messages.success(request, "Déconnexion réussie")
    return redirect('connection')
