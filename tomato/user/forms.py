from django import forms

from user.models import user
from user.models import profile

class UserForm(forms.ModelForm):
    class Meta:
        model = user
        fields = ["name",]

class ProfileFrom(forms.ModelForm):
    class Meta:
        model = profile
        fields = ["dating_location",]