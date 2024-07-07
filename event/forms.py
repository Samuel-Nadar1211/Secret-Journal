from django import forms
from .models import Events

class EventForm (forms.ModelForm):
    class Meta:
        model = Events
        fields = ['title', 'date', 'is_anniversary', 'remark']