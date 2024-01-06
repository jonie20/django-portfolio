from django.contrib import admin
from django.urls import path, re_path
from . import views
from django.contrib.auth import views as auth_views

app_name = "portfolioapp"
urlpatterns = [
    path('', views.home, name="home"),
    path('login-user', views.login_user, name="login-user"),
    # path('', views.home, name="home"),
    path('logout-user', views.logoutuser, name="logoutuser"),
    path('user-register', views.registerUser, name="register-user"),
    path('admin-panel', views.admin, name="admin-panel"),
    path('insert-experience',views.insertExperience, name="insertExperience"),
    path('insert-education',views.insertEducation, name="insertEducation"),
    path('insert-testimony',views.insertTestimony, name="insertTestimony"),
    path('insert-skill',views.insertSkill, name="insertSkill"),
    path('insert-project',views.insertProject, name="insertProject"),
    path('insert-badge',views.insertBadge, name="insertBadge"),
    path('contact/', views.contact, name="contact"),
    path('mpesa', views.stkpush, name="pay"),
]