# Generated by Django 5.0.4 on 2024-09-21 15:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_watchedcourse'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_file', models.FileField(blank=True, null=True, upload_to='videos/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('educator_upload', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='videos', to='home.educatorupload')),
            ],
        ),
    ]