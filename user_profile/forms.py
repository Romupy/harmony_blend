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

    current_image = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialiser le champ current_image avec le chemin de l'image actuelle
        if self.instance and self.instance.image:
            self.fields['current_image'].initial = self.instance.image.url
