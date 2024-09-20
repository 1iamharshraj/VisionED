from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import CreateView

from home.forms import EducatorSignUpForm, StudentSignUpForm, AdminSignUpForm, LoginForm

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
    template_name = 'users/register.html'
    success_url = '/home/'

    def get_form_class(self):
        # Determine which form to use based on account_type in the GET parameters
        account_type = self.request.GET.get('account_type')

        if account_type == 'admin':
            return AdminSignUpForm
        elif account_type == 'student':
            return StudentSignUpForm
        elif account_type == 'educator':
            return EducatorSignUpForm
        else:
            # Default or handle error if no valid account type is provided
            return StudentSignUpForm  # Or any other default form

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