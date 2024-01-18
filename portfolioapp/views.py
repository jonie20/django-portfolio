import os
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings

import requests
from requests.auth import HTTPBasicAuth
from . credentials import MpesaAccessToken, LipanaMpesaPpassword

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
import json, datetime
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect

from PIL import Image,ImageDraw
from django.core.files.base import ContentFile
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

from .models import Experience, Education, Testimonial, Projects, Badge, Skills, Emails

# Create your views here.

def resize_to_circle(image):
    img = Image.open(image)

    mask = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0,0, img.size[0],img.size[1]), fill=255)

    result = Image.new ('RGBA', img.size, (255,255,255,0))
    result.paste(img,mask=mask)

    output_buffer = BytesIO()
    result.save(output_buffer, format='PNG')

    output_FILE = InMemoryUploadedFile(
        output_buffer,
        None,
        f'{image.name.split(".")[0]}_circle.png',
        'image/png',
        output_buffer.tell(),
        None
    )
    return output_FILE


def home(request):

    testimony=Testimonial.objects.all()
    education = Education.objects.all().order_by('-id')
    experience = Experience.objects.all().order_by('-id')
    project = Projects.objects.all()
    skills = Skills.objects.all()
    badge = Badge.objects.all()
    context = {
        'education': education,
        'testimony': testimony,
        'project':project,
        'experience': experience,
        'skill': skills,
        'badge' : badge,
    }  
    return render(request,"index.html",context)


def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('portfolioapp:admin-panel')
        else:
            return redirect('portfolioapp:login-user')


        pass
    else:
        return render (request, 'login.html', {})


def logoutuser(request):
    logout(request)
    return redirect('/')



def registerUser(request):
    user = request.user
    if user.is_authenticated:
        return redirect('portfolioapp:home')
    if request.method == 'POST':
        data = request.POST
        form = UserRegistration(data)
        if form.is_valid():
            form.save()
            newUser = User.objects.all().last()
            try:
                profile = UserProfile.objects.get(user = newUser)
            except:
                profile = None
            if profile is None:
                UserProfile(user = newUser, dob= data['dob'], contact= data['contact'], address= data['address'], avatar = request.FILES['avatar']).save()
            else:
                UserProfile.objects.filter(id = profile.id).update(user = newUser, dob= data['dob'], contact= data['contact'], address= data['address'])
                avatar = AddAvatar(request.POST,request.FILES, instance = profile)
                if avatar.is_valid():
                    avatar.save()
            username = form.cleaned_data.get('username')
            pwd = form.cleaned_data.get('password1')
            loginUser = authenticate(username= username, password = pwd)
            login(request, loginUser)
            return redirect('admin-panel')
        else:
            context['reg_form'] = form

    return render(request,'signup.html')




def logoutuser(request):
    logout(request)
    return redirect('/')

@login_required
def admin(request):
    return render(request, 'admin.html')

def insertExperience(request): 
    if request.method=="POST":
        experience_title=request.POST.get('experience_title')
        experience_duration=request.POST.get('experience_duration')
        message=request.POST.get('message')

        
        query=Experience(experience_title=experience_title, experience_duration=experience_duration, experience_text=message)
        query.save()
        return redirect("/")

    return render('admin.html')

def insertEducation(request):
    if request.method=="POST":
        education_title = request.POST.get('education_title')
        course = request.POST.get('course')
        duration = request.POST.get('duration')
        message = request.POST.get('message')

        query = Education(education_title=education_title, course=course, education_duration=duration, education_text=message)
        query.save()

        return redirect('/')

    return render('admin.html')

def insertTestimony(request):
    if request.method=="POST":
        testimonial_name = request.POST.get('testimonial-name')
        message = request.POST.get('message')

        if len(request.FILES) !=0:
            testimonial_image = request.FILES['testimonial-image']
            resized_image = resize_to_circle(testimonial_image)
        
        query = Testimonial(testimonial_name=testimonial_name, testimonial_image=resized_image, testimonial_text=message)
        query.save()

        return redirect('/')

    return render('admin.html')

def insertSkill(request):
    if request.method=="POST":
        skill_name = request.POST.get('skill-name')
        skill_value = request.POST.get('skill-value')

        query = Skills( skill_name = skill_name, skill_value = skill_value )
        query.save()

        return redirect('/')

    return render('admin.html')

def insertProject(request):
    if request.method=="POST":
        project_title = request.POST.get('project-name')
        project_category = request.POST.get('project-category')
        project_url = request.POST.get('project-url')
        

        if len(request.FILES) !=0:
            project_image = request.FILES['project-image']
        
        query = Projects(project_title=project_title, project_category=project_category, project_url=project_url, project_image=project_image)
        query.save()

        return redirect('/')

    return render('admin.html')

def insertBadge(request):
    if request.method=="POST":
        badge_url = request.POST.get('badge-url')
        

        if len(request.FILES) !=0:
            badge_image = request.FILES['badge-image']
        
        query = Badge(badge_url=badge_url, badge_image=badge_image)
        query.save()

        return redirect('/')

    return render('admin.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('fullname')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if email and message and name:
            try:
                query = Emails(name = name, email=email, message=message)
                query.save()
                
                subject = 'Mail form Portfolio Website'
                email_message = f'Name : {name}\nEmail: {email}\nMessage: {message}'
                
                send_mail(subject, email_message, email, [settings.EMAIL_HOST_USER], fail_silently=False)
            except BadHeaderError:
                return HttpResponse("Inavlid header found.")
                return HttpResponseRedirect('/')
        else:
            return HttpResponse("Make sure all fields are entered")
            return redirect('/')

    return render(request, 'index.html')

def pay(request):
    if request.method =="POST":
        phone = request.POST['phone']
        amount = request.POST['amount']
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        request = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": "Johnstone Kipkosgei Cheruiyot",
            "TransactionDesc": "Web development Charges..."
        }

    response = requests.post(api_url, json=request, headers=headers)
    return HttpResponse("success")

def stkpush(request):

    if request.method =="POST":
        phone = request.POST['phone']
        amount = request.POST['amount']
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        request = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": "Johnstone Kipkosgei Cheruiyot",
            "TransactionDesc": "Web development Charges..."
        }

    response = requests.post(api_url, json=request, headers=headers)
    return render(request,'pay.html')
