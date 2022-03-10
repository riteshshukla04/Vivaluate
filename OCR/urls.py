from django.contrib import admin
from django.urls import path,include
from . import views






urlpatterns = [
    #path('', views.index),
    path("login/",view=views.Login),
    path("",views.Test),
    path("logout/",views.logoutUser),
    path("add/",views.addStudent)

]