from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, FormView, TemplateView

from home.forms import LoginForm, SignUpForm, EducatorUploadForm
import requests
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View
from .forms import LoginForm
from .models import EducatorUpload, WatchedCourse


class StudentVidView(View):
    def get(self, request, video_id):
        # URL for the Node.js server, fetching the video based on video_id
        node_server_url = f"http://localhost:3000/{video_id}.mp4"

        # try:
        #     # Make a request to the Node.js server to get the video details
        #     response = requests.get(node_server_url, stream=True)
        #     response.raise_for_status()  # Raise an exception for HTTP errors
        #
        #     # If you just want to get the URL for the video, you can directly return it to the template.
        #     video_data = node_server_url
        # except requests.exceptions.RequestException as e:
        #     # Handle errors, such as connection issues
        #     print(f"Error fetching video data: {e}")
        #     video_data = None

        video_data = node_server_url

        # Render the template and pass the video data
        return render(request, "students/StuVidPlayer.html", {'video_data': video_data})
class EducatorCourseView(View):
    def get(self, request):
        return render(request,"educator/EduCourses.html")
class StudentHomeView(TemplateView):
    template_name = 'students/Stuhome.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the recent watched courses for the logged-in student
        context['recently_watched_courses'] = WatchedCourse.objects.filter(student=self.request.user).order_by('-watched_at')[:5]  # Last 5 watched courses
        return context

class StudentCourseView(View):
    def get(self, request):
        return render(request,"students/StuCourses.html")


class LoginView(View):
    def get(self, request):
        # If the user is already logged in, log them out
        if request.user.is_authenticated:
            logout(request)

        # Render the login form for GET request
        form = LoginForm()

        return render(request, 'authenticate/login.html', {'form': form})

    def post(self, request):
        # Handle the form submission (POST request)
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Authenticate the user
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)  # Log the user in

                # Redirect based on account type
                if user.account_type == 'admin':
                    return redirect('admin_home')
                elif user.account_type == 'student':
                    return redirect('stu_home')
                elif user.account_type == 'educator':
                    return redirect('edu_home')
                return redirect('home')
            else:
                # Add an error if authentication fails
                form.add_error(None, 'Invalid username or password')

        return render(request, 'authenticate/login.html', {'form': form})

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
            return redirect('admin_home')
        elif user.account_type == 'student':
            return redirect('stu_home')
        elif user.account_type == 'educator':
            return redirect('edu_home')
        else:
            return redirect(self.success_url)


class EducatorHomeView(CreateView):
    model = EducatorUpload
    form_class = EducatorUploadForm
    template_name = 'educator/educatorhome.html'
    success_url = '/educator_home/'

    def form_valid(self, form):
        # Set the educator field to the current user
        form.instance.educator = self.request.user
        form.save()  # Save the form instance
        print(form.cleaned_data)  # Debugging line
        return super().form_valid(form)

    def form_invalid(self, form):
        # This method is called when the form is invalid
        print(form.errors)  # Debugging line
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch all courses uploaded by the current educator
        context['educator_uploads'] = EducatorUpload.objects.filter(educator=self.request.user)
        return context