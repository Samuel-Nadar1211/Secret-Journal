from django import forms
from .models import User

class UserForm (forms.ModelForm):
    password = forms.CharField (widget = forms.PasswordInput)
    password_confirm = forms.CharField (widget = forms.PasswordInput, label='Re-enter Password')

    class Meta:
        model = User
        fields = ['name', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords don't match. Please enter again.")
