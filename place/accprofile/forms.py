from django import forms
from .models import Profile, CoinsModel


class CoinsForm(forms.ModelForm):
    class Meta:
        model = CoinsModel
        fields = ('price',)


class EditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('photo', 'bio', 'subprice')


class SignupForm(forms.Form):

    def signup(self, request, user):
        profile = Profile()
        profile.user = user
        user.save()
        profile.save()
