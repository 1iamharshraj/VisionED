from django import forms
from home.models import CustomUser


class AdminSignUpForm(forms.ModelForm):
    # Define the form fields for the admin sign-up form
    account_type = forms.CharField(max_length=20, widget=forms.HiddenInput(), initial='admin')
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'username', 'password']


class StudentSignUpForm(forms.ModelForm):
    # Define the form fields for the developer sign-up form
    account_type = forms.CharField(max_length=20, widget=forms.HiddenInput(), initial='developer')
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'username', 'password']


class EducatorSignUpForm(forms.ModelForm):
    # Define the form fields for the project manager sign-up form
    account_type = forms.CharField(max_length=20, widget=forms.HiddenInput(), initial='project_manager')
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'username', 'password']


class LoginForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }