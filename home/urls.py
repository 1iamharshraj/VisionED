from django.conf.urls.static import static
from django.urls import path

from VisionED import settings
from . import views

urlpatterns = [
    path('', views.LoginView.as_view(), name='home'),
    path('login',views.LoginView.as_view(),name='login'),
    path("edu_home",views.EducatorHomeView.as_view(),name='edu_home'),
    path("stu_home",views.StudentHomeView.as_view(),name='stu_home'),
    path("stu_course",views.StudentCourseView.as_view(),name='stu_course')
]
