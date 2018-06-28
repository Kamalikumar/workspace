from django import forms
from django.forms import ModelForm

from models import *

class SmTrnregisterForm(forms.ModelForm):
    class Meta:
        model =  SmTrnregister
        fields = ["entryid","startdate","entryby","category","description","importance"]

