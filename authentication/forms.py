from django import forms

from user_profile.models import UserProfile


class LoginForm(forms.Form):
    email = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput())


class RegisterForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = (
            'image',
            'presentation',
            'registration_date',
            'skin_brightness',
            'skin_info',
        )

    email = forms.CharField(max_length=30)
    password = forms.CharField(
        label="Mot de passe", widget=forms.PasswordInput()
    )
    password_confirmation = forms.CharField(
        label="Confirmation du mot de passe", widget=forms.PasswordInput()
    )
