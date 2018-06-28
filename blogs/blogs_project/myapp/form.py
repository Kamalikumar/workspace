from django.forms import ModelForm
from  django.core.exceptions import NON_FIELD_ERRORS
from .models import Todo

class Todo_forms(ModelForm):
    class Meta:
        model=Todo
        fields=['text','is_completed']

form =Todo_forms()







