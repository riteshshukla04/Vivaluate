from operator import mod
from re import L
from statistics import mode
from django.db import models
from django.contrib.auth.models import User


class Teacher(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    def __str__(self) -> str:
        return self.name
        

class Student(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    register_number=models.CharField(max_length=200,null=True,blank=True)
    def __str__(self) -> str:
        return self.name

class Classroom(models.Model):
    code=models.CharField(max_length=200,null=True,blank=True,unique=True)
    name=models.CharField(max_length=200,null=True,blank=True)
    description=models.TextField(null=True,blank=True)
    student=models.ManyToManyField(Student)
    teacher=models.ForeignKey(Teacher,on_delete=models.CASCADE)
    def __str__(self) -> str:
        return self.name

class Question(models.Model):
    question_desc=models.CharField(max_length=200)
    correct_answer=models.CharField(max_length=200)
    marks=models.FloatField()
    def __str__(self) -> str:
        return self.question_desc

    
class Test(models.Model):
    name=models.CharField(max_length=200,null=True,blank=True)
    classroom=models.ForeignKey(Classroom,on_delete=models.CASCADE)
    questions=models.ManyToManyField(Question)
    def __str__(self) -> str:
        return self.name

class Answer(models.Model):
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
    #test=models.ForeignKey(Test,on_delete=models.CASCADE)
    submitted=models.ImageField()
    awarded_marks=models.FloatField(null=True,default=True)
    def __str__(self) -> str:
        return self.question.question_desc






