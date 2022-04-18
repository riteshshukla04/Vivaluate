
import imp
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,HttpResponse,redirect
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
import pytesseract
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

from OCR.cosine import cosineAnswer
from .models import *
from .forms import CreateUserForm
import random,string
from .decorators import *
from .googlevision import GoogleOCR


@authenticated_user
def logoutUser(request):
    logout(request)
    return redirect("/login")


@csrf_exempt
@unauthenticated_user
def Login(request):
    context={}
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        
        user=authenticate(request,username=username,password=password)
        
        if user is not None:
            login(request,user)
            if user.groups.filter(name='Teacher'):
                return redirect("/teacher")
            else:
                return redirect("/student")
        else:
           messages.info(request,"Username or password incorrect")             
     
    return render(request,'login.html',context)


@authenticated_user
def addStudent(request):
    if(request.method=="POST"):
        try:
            code=request.POST["code"]
            classroom=Classroom.objects.get(code=code)
            student=Student.objects.get(user=request.user)
            classroom.student.add(student)
            classroom.save()
        except:
             messages.info(request,"Doesnt exist")  
        
        return redirect("/student")
    return render(request,"tarpg.html")

""" def TestFunction(request):
    if request.user.groups.filter(name='Student').exists():
         classroom=Classroom.objects.filter(student=Student.objects.get(user=request.user))
         return render(request,"Test.html",{"classroom":classroom})
    if request.user.groups.filter(name='Teacher').exists():
         classroom=Classroom.objects.filter(teacher=Teacher.objects.get(user=request.user))
         return render(request,"Test.html",{"classroom":classroom})

    return render(request,"Test.html") """
    

def index(request):
    s=""
    if (request.method=="POST"):
        img=request.FILES["answersheet"]
     
        
        s=GoogleOCR(img)
        
        

    return render(request,"index.html",{"s":s})


@csrf_exempt
@unauthenticated_user
def registerPage(request):
    form=CreateUserForm()
    
    if request.method=="POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            group=Group.objects.get(name='Student')
            user.groups.add(group)
            name=request.POST["Name"]
            login(request,user)
            s=Student.objects.create(user=user,name=name)
            s.save()
            messages.success(request,"Account was created")
            return redirect("/")
    context={'form':form}
    return render(request,'register.html',context)\




@csrf_exempt
@unauthenticated_user
def registerPageTeacher(request):
    form=CreateUserForm()
    
    if request.method=="POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            group=Group.objects.get(name='Teacher')
            user.groups.add(group)
            name=request.POST["Name"]
            login(request,user)
            s=Teacher.objects.create(user=user,name=name)
            s.save()
            messages.success(request,"Account was created")
            return redirect("/")
    context={'form':form}
    return render(request,'register.html',context)


def addClassroom(request):
    s=''.join(random.choices(string.ascii_uppercase+string.ascii_lowercase+ string.digits, k=6))
    if request.method=="POST":
        name=request.POST["classname"]
        s=Classroom.objects.create(teacher=Teacher.objects.get(user=request.user),code=s,name=name)
        s.save()
        return redirect("/teacher")
    return render(request,'addclass.html',{"s":s})


@allowed_users(["Student"])
def classlist(request):
    s=Classroom.objects.filter(student=Student.objects.get(user=request.user))
    return render(request,'student_landing_page.html',{"s":s})


@allowed_users(["Teacher"])
def TeacherLandingPage(request):
    s=Classroom.objects.filter(teacher=Teacher.objects.get(user=request.user))
    return render(request,'teacher_landing_page.html',{"s":s})

@unauthenticated_user
def MainIndex(request):
    return render(request,"tarplanding.html")


def studentList(request,pk):
    s=Classroom.objects.get(id=pk)
    test=Test.objects.filter(classroom=Classroom.objects.get(id=pk))
    t=s.student.all()
    
    return render(request,"studentList.html",{"t":t,"pk":pk,"test":test,"s":s})



def createTest(request,pk):
    if request.method=="POST":
        name=request.POST["name"]
        test=Test.objects.create(name=name,classroom=Classroom.objects.get(id=pk))
        test.save()
        return redirect(f"/classlist/{pk}")
    return render(request,"TestList.html")


def TestList(request,pk):
    test=Test.objects.filter(classroom=Classroom.objects.get(id=pk))
    return render(request,'TestList.html',{"test":test})


def questionList(request,pk,pk1):
    test=Test.objects.get(id=pk)
    classroom=Classroom.objects.get(id=pk1)
    question=test.questions.all()
    return render(request,"questionList.html",{"question":question,"pk":pk,"pk1":pk1,"test":test})


def createQuestion(request,pk,pk1):
    if request.method=="POST":
        name=request.POST["name"]
        marks=request.POST["marks"]
        answer=request.POST["answer"]
        question=Question.objects.create(question_desc=name,correct_answer=answer,marks=marks)
        question.save()
        test=Test.objects.get(id=pk)
        test.questions.add(question)
        test.save()
        return redirect(f"/questionlist/{pk}/{pk1}")
    return render(request,"questionList.html")

def TestListStudent(request,pk):
    test=Test.objects.filter(classroom=Classroom.objects.get(id=pk))
    return render(request,'Test_List_Student.html',{"test":test})


def questionListStudent(request,pk):
    test=Test.objects.get(id=pk)
    question=test.questions.all()
    return render(request,"question_list_student.html",{"question":question,"pk":pk})

def Upload_Answer(request,pk,pk1):
    if (request.method=="POST"):
        question=Question.objects.get(id=pk)
        
        image=request.FILES["file"]
        s=GoogleOCR(image)
        print(s)
        s=cosineAnswer(question.correct_answer,s)
        ans=Answer.objects.filter(question=question,student=Student.objects.get(user=request.user)).count()
        ans1=Answer.objects.filter(question=question,student=Student.objects.get(user=request.user))
        s=s*(question.marks)
        if((ans)>0):
            ans1.delete()
        
        answer=Answer.objects.create(question=question,student=Student.objects.get(user=request.user),submitted=image,awarded_marks=s)
        answer.save()
        return redirect(f"/questionlists/{pk1}")
        
    return render(request,"uploadAnswer.html")


def student_list_question(request,pk):
    question=Question.objects.get(id=pk)
    answer=Answer.objects.filter(question=Question.objects.get(id=pk))
    return render(request,"student_List_Question.html",{"answer":answer,"question":question})

def authenticator(request):
    if request.user.groups.filter(name='Teacher'):
                return redirect("/teacher")
    else:
                return redirect("/student")


def getStudent(request,pk,pk1):
    test=Test.objects.get(id=pk)
    question=test.questions.all()
    l=[]
    for i in question:
        m=[]
        answer=Answer.objects.filter(question=i)
        
    return HttpResponse("Hello World")
    