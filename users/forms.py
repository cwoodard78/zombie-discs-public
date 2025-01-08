from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput, 
        label="Password",
        help_text="Your password must meet the complexity requirements."
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        # Use Django's built-in password validators
        validate_password(password)
        return password