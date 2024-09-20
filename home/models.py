from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import CreateView

from home.forms import EducatorSignUpForm, StudentSignUpForm, AdminSignUpForm, LoginForm


class CustomUser(AbstractUser):
    ACCOUNT_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('student', 'Student'),
        ('educator', 'Educator')
    )
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPE_CHOICES)


class LoginView(View):
    def get(self, request):
        # Render the login form
        form = LoginForm()
        return render(request, 'users/login.html', {'form': form})

    def post(self, request):
        # Get the form data from the request
        form = LoginForm(request.POST)

        # Validate the form data
        if form.is_valid():
            # Get the username and password from the form
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Authenticate the user
            user = authenticate(request, username=username, password=password)

            # If the user is authenticated, log them in and redirect to the homepage
            if user is not None:
                login(request, user)
                if user.account_type == 'admin':
                    return redirect('admin_home')
                elif user.account_type == 'developer':
                    return redirect('developer_home')
                elif user.account_type == 'project_manager':
                    return redirect('projectmanager_home')
                return redirect('home')

            # If the user is not authenticated, render the login form again with an error message
            else:
                form.add_error(None, 'Invalid username or password')
                return render(request, 'users/login.html', {'form': form})
        else:
            return render(request, 'users/login.html', {'form': form})


class LogoutView(View):
    def get(self, request):
        # Log out the user and redirect to the login page
        logout(request)
        return redirect('home')


class AdminSignUpView(CreateView):
    form_class = AdminSignUpForm
    template_name = 'users/admin_signup.html'
    success_url = '/admin_home/'

    def form_valid(self, form):
        # Create the user and log them in
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)


class StudentSignUpView(CreateView):
    form_class = StudentSignUpForm
    template_name = 'users/developer_signup.html'
    success_url = '/developer_home/'

    def form_valid(self, form):
        # Create the user and log them in
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)


class EducatorSignUpView(CreateView):
    form_class = EducatorSignUpForm
    template_name = 'users/projectmanager_signup.html'
    success_url = '/projectmanager_home/'

    def form_valid(self, form):
        # Create the user and log them in
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)