from django import forms

from home.models import CustomUser

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


class LoginForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }