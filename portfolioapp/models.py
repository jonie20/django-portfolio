from django.db import models

from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone

# Create your models here.


class Experience(models.Model):
    experience_title = models.CharField(max_length=250)
    experience_duration = models.CharField(max_length=250)
    experience_text = models.TextField(blank=False, null = False)

    def __str__(self):
        return self.experience_title

class Education(models.Model):
    education_title = models.CharField(max_length=250)
    course = models.CharField(max_length=250)
    education_duration = models.CharField(max_length=250)
    education_text = models.TextField(blank=False, null = False)

    def __str__(self):
        return self.education_title

class Testimonial(models.Model):
    testimonial_name = models.CharField(max_length=250)
    testimonial_image = models.ImageField(blank=True, null=True,upload_to='testimonials/images', default="logo.png")
    testimonial_text = models.TextField(blank=False, null = False)
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.testimonial_name

class Projects(models.Model):
    project_title = models.CharField(max_length=250)
    project_category = models.TextField(blank=False, null=False)
    project_url = models.URLField(max_length=2000, default="https://github.com/jonie20")
    project_image = models.ImageField(blank=True, null=True,upload_to='projects/images', default="default_project.jpg")
    
    def __str__(self):
        return self.project_title

class Badge(models.Model):
    badge_url = models.URLField(max_length=2000, default="https://github.com/jonie20")
    badge_image = models.ImageField(blank=True, null=True,upload_to='Badges/images', default="default_project.jpg")

class Skills(models.Model):
    skill_name = models.CharField(max_length=250)
    skill_value = models.IntegerField()

class Emails(models.Model):
    name = models.CharField(max_length=250)
    email = models.CharField(max_length=250)
    message = models.TextField(blank=False, null = False)   