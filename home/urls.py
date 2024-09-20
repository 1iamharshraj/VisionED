from django.conf.urls.static import static
from django.urls import path

from VisionED import settings
from . import views

urlpatterns = [
    path('', views.SignUpView.as_view(), name='home'),
    path('login',views.LoginView.as_view(),name='login'),
    path("student_home",views.EducatorHomeView.as_view(),name='student_home')
]
