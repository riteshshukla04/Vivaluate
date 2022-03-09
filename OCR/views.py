from django.http import HttpResponse
from django.shortcuts import render,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
import pytesseract

# Create your views here.

def index(request):
    s=""
    if (request.method=="POST"):
        img=request.FILES["answersheet"]
        img=Image.open(img)
        s=(pytesseract.image_to_string(img))
        

    return render(request,"index.html",{"s":s})