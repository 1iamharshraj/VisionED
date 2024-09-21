from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, FormView, TemplateView

from django.http import JsonResponse
from home.forms import LoginForm, SignUpForm, EducatorUploadForm

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View
from .forms import LoginForm
from .models import EducatorUpload, WatchedCourse

import google.generativeai as genai
import requests
import os
from PyPDF2 import PdfReader
# import chromadb
# import chromadb.utils.embedding_functions as embedding_functions
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

class StudentProfileView(TemplateView):
        template_name = 'students/Profile.html'


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



class SignUpView1(CreateView):
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
    success_url = '/edu_home/'

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




def chatbot_response(request):
    if request.method == 'POST':
        message = request.POST.get('message')

        # Use a chatbot model (like an NLP library or a machine learning model) to generate a response
        genai.configure(api_key="AIzaSyBms6uYpRx7lCBGm5claKd5R-3cH235v8M")

        def split_text_recursively(text, max_length=1000, chunk_overlap=0):
            chunks = []
            start = 0  # start at the beginning
            text_length = len(text)  # figure out how long is the text provided.
            while start < text_length:  # keep going until we have looked at all the text
                end = start + max_length
                if end < text_length:  # if we are not yet at the end of the text
                    end = text.rfind(' ', start, end) + 1  # end the chunk at an empty space.

                    if end <= start:  # if there is no space, then just split at the max length.
                        end = start + max_length
                chunk = text[start:end].strip()  # take the text from start to end and remove extra spaces.

                if chunk:
                    chunks.append(chunk)

                start = end - chunk_overlap  # moving the start position forward minus any overlaps.

                if start >= text_length:  # if we have reached the end of the text
                    break
            return chunks

        def load_pdf(file_path):
            pdf_reader = PdfReader(file_path)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text

        def download_pdf(url, save_path):
            response = requests.get(url)
            response.raise_for_status()

            with open(save_path, "wb") as file:
                file.write(response.content)

        def build_escaped_context(context):
            escaped_context = ""
            for item in context:
                escaped_context += item + "\n\n"
            return escaped_context

        def find_relevant_context(query, db, n_results=3):
            results = db.query(query_texts=[query], n_results=n_results)
            escaped_context = build_escaped_context(results['documents'][0])
            return escaped_context

        def generate_answer_from_gemini(prompt):
            model = genai.GenerativeModel('gemini-1.5-flash-latest')
            result = model.generate_content(prompt)
            return result

        def create_prompt_for_gemini(query, context):
            prompt = f"""
          You are a helpful agent that answers questions using the text from the context below.
          Both the question and the context is shared with you and you should answer the
          question basis the context. If the context does not have enough information
          for you to answer the question correctly, inform about the absence of relevant
          context as part of your answer.

          Question : {query}
          \n
          Context : {context}
          \n
          Answer :
          """
            return prompt

        save_path = "/content/1.pdf"
        pdf_text = load_pdf(save_path)
        chunks = split_text_recursively(pdf_text, max_length=2000, chunk_overlap=200)
        google_ef = embedding_functions.GoogleGenerativeAiEmbeddingFunction(api_key="AIzaSyBms6uYpRx7lCBGm5claKd5R-3cH235v8M")
        client = chromadb.PersistentClient(path="embeddings/gemini")

        collection = client.get_or_create_collection(name="pdf_rag", embedding_function=google_ef)

        for i, d in enumerate(chunks):
            collection.add(documents=[d], ids=[str(i)])
        context = find_relevant_context("role of encoders", collection)
        escaped_context = build_escaped_context(context)
        answer = generate_answer_from_gemini(f"{message}")
        response = answer.text
        #response = "This is a response to: "
        return JsonResponse({'response': response})

