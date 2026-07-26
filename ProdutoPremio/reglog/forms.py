from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User

class RegisterForms(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password',  ]
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Nome', 'minlength': 5, 'maxlength': 50, 'required': 'true', 'type': 'text'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email', 'minlength': 10, 'maxlength': 254, 'required': 'true', 'type': 'email'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Senha', 'minlength': 8,'maxlength': 64, 'required': 'true', 'type': 'password'}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Nome ja existente, tente outro")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("email ja existente, tente outro")

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
    
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("email ja existente, tente outro")
    
        return email

class LoginForms(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Email', 'minlength': 10, 'maxlength': 254, 'required': 'true', 'type': 'email'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Senha', 'minlength': 8,'maxlength': 64, 'required': 'true', 'type': 'password'}),
        }