from django import forms

from user_profile.models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('registration_date', 'skin_brightness', 'skin_info',)


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('registration_date', 'skin_brightness', 'skin_info',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)