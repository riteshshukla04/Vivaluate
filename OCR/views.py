
import imp
from django.http import HttpResponse
from django.shortcuts import render,HttpResponse,redirect
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
import pytesseract

from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import *



def logoutUser(request):
    logout(request)
    return redirect("/")


@csrf_exempt
def Login(request):
    context={}
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        
        user=authenticate(request,username=username,password=password)
        
        if user is not None:
            login(request,user)
            return redirect("/")
        else:
           messages.info(request,"Username or password incorrect")             
     
    return render(request,'login.html',context)




def addStudent(request):
    if(request.method=="POST"):
        code=request.POST["code"]
        classroom=Classroom.objects.get(id=code)
        student=Student.objects.get(user=request.user)
        classroom.student.add(student)
        classroom.save()
        return render(request,"addStudent.html")
    return render(request,"addStudent.html")

def Test(request):
    if request.user.groups.filter(name='Student').exists():
         classroom=Classroom.objects.filter(student=Student.objects.get(user=request.user))
         return render(request,"Test.html",{"classroom":classroom})
    if request.user.groups.filter(name='Teacher').exists():
         classroom=Classroom.objects.filter(teacher=Teacher.objects.get(user=request.user))
         return render(request,"Test.html",{"classroom":classroom})

    return render(request,"Test.html")
    

def index(request):
    s=""
    if (request.method=="POST"):
        img=request.FILES["answersheet"]
        img=Image.open(img)
        s=(pytesseract.image_to_string(img))
        

    return render(request,"index.html",{"s":s})