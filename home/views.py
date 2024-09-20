from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import CreateView

from home.forms import  LoginForm, SignUpForm


class LoginView(View):
    def get(self, request):
        # Render the login form
        form = LoginForm()
        return render(request, 'authenticate/login.html', {'form': form})

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
                elif user.account_type == 'student':
                    return redirect('student_home')
                elif user.account_type == 'educator_manager':
                    return redirect('educator_home')
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

class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'users/register.html'  # You can reuse this for different account types
    success_url = ''  # Redirect based on account type if necessary

    def form_valid(self, form):
        # Create the user and log them in
        user = form.save()
        login(self.request, user)

        # Redirect based on the account type
        if user.account_type == 'admin':
            return redirect('/admin_home/')
        elif user.account_type == 'student':
            return redirect('/student_home/')
        elif user.account_type == 'educator':
            return redirect('/educator_home/')
        else:
            return redirect(self.success_url)
