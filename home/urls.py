from django.urls import path
from . import views

urlpatterns = [
    path('', views.SignUpView.as_view(), name='home'),
]