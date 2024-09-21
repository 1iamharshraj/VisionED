from django.conf.urls.static import static
from django.urls import path

from VisionED import settings
from . import views

urlpatterns = [
    path('', views.SignUpView.as_view(), name='home'),
    path('register',views.SignUpView1.as_view(),name='register'),
    path('login',views.LoginView.as_view(),name='login'),
    path("edu_home",views.EducatorHomeView.as_view(),name='edu_home'),
    path("edu_course",views.EducatorCourseView.as_view(),name='edu_course'),
    path("stu_home",views.StudentHomeView.as_view(),name='stu_home'),
    path('chatbot/', views.chatbot_response, name='chatbot_response'),
    path("stu_course",views.StudentCourseView.as_view(),name='stu_course'),
    path("stu_vid/<int:video_id>/", views.StudentVidView.as_view(), name='stu_vid'),
    path("stu_prof", views.StudentProfileView.as_view(), name='stu_prof'),
    path('edu_prof',views.EducatorProfileView.as_view(),name='edu_prof')
]
