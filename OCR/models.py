from operator import mod
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
    def __str__(self) -> str:
        return self.name

class Classroom(models.Model):
    name=models.CharField(max_length=200,null=True,blank=True)
    student=models.ManyToManyField(Student)
    teacher=models.ForeignKey(Teacher,on_delete=models.CASCADE)
    def __str__(self) -> str:
        return self.name



