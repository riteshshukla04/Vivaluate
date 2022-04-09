from lib2to3.pygram import pattern_grammar
from venv import create
from django.contrib import admin
from django.urls import path,include
from . import views






urlpatterns = [
    #path('', views.index),
    path("login/",view=views.Login),
    path("student/",views.classlist),
    path("logout/",views.logoutUser),
    path("add/",views.addStudent),
    path("register/student",views.registerPage),
    path("register/teacher",views.registerPageTeacher),
    path("addclass/",views.addClassroom),
    path('teacher/',views.TeacherLandingPage),
    path("",views.MainIndex),
    path("ocr/",views.index),
    path("classlist/<str:pk>",views.studentList),
    path("createtest/<str:pk>",views.createTest),
    path("testlist/<str:pk>",views.TestList),
    path("questionlist/<str:pk>",views.questionList),
     path("createquestion/<str:pk>",views.createQuestion),
     path("testlists/<str:pk>",views.TestListStudent),
     path("questionlists/<str:pk>",views.questionListStudent),
     path("uploadanswer/<str:pk>/<str:pk1>",views.Upload_Answer),


]