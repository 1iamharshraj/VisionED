from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class CustomUser(AbstractUser):
    ACCOUNT_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('student', 'Student'),
        ('educator', 'Educator')
    )
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPE_CHOICES)

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Change the related_name to avoid conflict with auth.User
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions_set',  # Change the related_name to avoid conflict with auth.User
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )
    class Meta:
        app_label = 'home'


class EducatorUpload(models.Model):
    educator = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    ppt_file = models.FileField(upload_to='uploads/ppt/')
    image = models.ImageField(upload_to='uploads/img/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class WatchedCourse(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='watched_courses')
    educator_upload = models.ForeignKey(EducatorUpload, on_delete=models.CASCADE)
    watched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} watched {self.educator_upload.title}"


class Video(models.Model):
    educator_upload = models.ForeignKey(EducatorUpload, on_delete=models.CASCADE, related_name='videos')
    video_file = models.FileField(upload_to='videos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Video for {self.educator_upload.title}"