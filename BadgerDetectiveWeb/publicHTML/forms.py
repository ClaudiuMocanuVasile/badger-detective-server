from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class ClientForm(forms.ModelForm):

    link = forms.CharField(
        widget = forms.TextInput(
            attrs = {}
        )
    )
    
    class Meta:

        model = Link
        fields = ['link']