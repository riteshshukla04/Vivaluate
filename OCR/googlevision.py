import cv2
import imutils
import json
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import requests
import time
from base64 import b64encode
from PIL import Image
from pylab import rcParams

from vivaluate.settings import GOOGLE_VISION_API_KEY


def GoogleOCR(image_file):
    finalanswer=""
    rcParams['figure.figsize'] = 10, 20
    def makeImageData(imgpath):
            img_req = None
       
           
            ctxt = b64encode(imgpath.read()).decode()

            img_req = {
                'image': {
                    'content': ctxt
                },
                'features': [{
                    'type': 'DOCUMENT_TEXT_DETECTION',
                    'maxResults': 1
                }]
            }
            return json.dumps({"requests": img_req}).encode()


    def requestOCR(ENDPOINT_URL, api_key, imgpath):
        imgdata = makeImageData(imgpath)
        response = requests.post(ENDPOINT_URL, 
                                data = imgdata, 
                                params = {'key': api_key}, 
                                headers = {'Content-Type': 'application/json'})
        return response

    ENDPOINT_URL = 'https://vision.googleapis.com/v1/images:annotate'
    api_key =GOOGLE_VISION_API_KEY
    img_loc = image_file

    result = requestOCR(ENDPOINT_URL, api_key, img_loc)
    if result.status_code != 200 or result.json().get('error'):
        print ("Error")
    else:
        result = result.json()['responses'][0]['textAnnotations']

    for index in range(len(result)):
        finalanswer+=(result[index]["description"])
    return finalanswer