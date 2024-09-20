
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

