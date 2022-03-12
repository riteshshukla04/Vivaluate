from django.contrib import admin
from django.urls import path,include
from . import views






urlpatterns = [
    #path('', views.index),
    path("login/",view=views.Login),
    path("",views.classlist),
    path("logout/",views.logoutUser),
    path("add/",views.addStudent),
    path("register/student",views.registerPage),
    path("register/teacher",views.registerPageTeacher),
    path("addclass",views.addClassroom),

]