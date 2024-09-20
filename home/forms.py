from django import forms
from django.contrib.auth import authenticate

from home.models import CustomUser, EducatorUpload

# Common Tailwind CSS classes
form_input_classes = ('mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm '
                      'focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm')
form_password_classes = ('mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm '
                         'focus:outline-none focus:ring-red-500 focus:border-red-500 sm:text-sm')

ACCOUNT_TYPE_CHOICES = [
    ('admin', 'Admin'),
    ('student', 'Student'),
    ('educator', 'Educator')
]


class SignUpForm(forms.ModelForm):
    # Account type field to choose between Admin, Student, and Educator
    account_type = forms.ChoiceField(choices=ACCOUNT_TYPE_CHOICES,
                                     widget=forms.Select(attrs={'class': form_input_classes}))

    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': form_input_classes}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': form_input_classes}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': form_input_classes}))
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': form_input_classes}))
    password = forms.CharField(max_length=128, widget=forms.PasswordInput(attrs={'class': form_password_classes}))

    class Meta:
        model = CustomUser
        fields = ['account_type', 'first_name', 'last_name', 'email', 'username', 'password']

    def save(self, commit=True):
        # Override the save method to handle different account types
        user = super().save(commit=False)
        user.account_type = self.cleaned_data['account_type']

        # Save the password properly hashed
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'mt-2 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm',
            'placeholder': 'Username',
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'mt-2 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm',
            'placeholder': 'Password',
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        # Authenticate the user
        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError("Invalid username or password.")
        return cleaned_data


class EducatorUploadForm(forms.ModelForm):
    title = forms.CharField(max_length=200, widget=forms.TextInput(attrs={
        'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm',
        'placeholder': 'Enter the title'
    }))

    description = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm',
        'placeholder': 'Enter a description'
    }))

    ppt_file = forms.FileField(widget=forms.ClearableFileInput(attrs={
        'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm',
    }))

    image = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={
        'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm',
    }))

    class Meta:
        model = EducatorUpload
        fields = ['title', 'description', 'ppt_file', 'image']

    def save(self, commit=True):
        # Save the instance and set the educator field
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance