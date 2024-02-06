from django import forms

from user_profile.models import UserProfile


class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('registration_date', 'skin_brightness', 'skin_info',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
