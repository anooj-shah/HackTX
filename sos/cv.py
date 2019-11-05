from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import TextOperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import TextRecognitionMode
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

import os
import sys
import time
import requests
import cv2
import json
import geocoder
from PIL import Image
import random

def runCV(webcam):
    data = []
    # Add your Computer Vision subscription key to your environment variables.
    if 'COMPUTER_VISION_SUBSCRIPTION_KEY' in os.environ:
        subscription_key = os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY']
    else:
        print("\nSet the COMPUTER_VISION_SUBSCRIPTION_KEY environment variable.\n**Restart your shell or IDE for changes to take effect.**")
        sys.exit()
    if 'COMPUTER_VISION_ENDPOINT' in os.environ:
        endpoint = os.environ['COMPUTER_VISION_ENDPOINT']

    video_name = 'man.mp4'
    if webcam:
        capture = cv2.VideoCapture(0)
    else:
        capture = cv2.VideoCapture(video_name)

    # Check if camera opened successfully
    if (capture.isOpened()== False): 
        print("Error: Video file wont open")
    
    # Read until video is completed
    frame_num = 0
    frame_increment = 50
    while(capture.isOpened()):
        ret, frame = capture.read()

        num_people = 0
        if ret == True:
            if frame_num % frame_increment == 0:
                cur_frame = frame.copy()
                cv2.imwrite("image.jpg", cur_frame)
                # Azure
                analyze_url = endpoint + "vision/v2.1/analyze"
                # Set image_path to the local path of an image that you want to analyze.
                image_path = "image.jpg"

                # Read the image into a byte array
                image_data = open(image_path, "rb").read()
                headers = {'Ocp-Apim-Subscription-Key': subscription_key,
                        'Content-Type': 'application/octet-stream'}
                params = {'visualFeatures': 'Categories,Description,Color,Objects'}
                response = requests.post(
                    analyze_url, headers=headers, params=params, data=image_data)
                response.raise_for_status()

                # Get data from azure
                analysis = response.json()
                # print(analysis)
                for obj in analysis["objects"]:
                    x = obj["rectangle"]["x"]
                    y = obj["rectangle"]["y"]
                    w = obj["rectangle"]["w"]
                    h = obj["rectangle"]["h"]
                    cv2.rectangle(cur_frame, (x,y), (x+w, y+h), (255, 0, 0), 3)
                    if obj["object"] == "person":
                        num_people += 1
                    print("This is a",obj["object"])
                if (len(analysis["description"]["captions"]) != 0):
                    image_caption = analysis["description"]["captions"][0]["text"].capitalize()
                    print(image_caption+"\n")

                g = geocoder.ip('me')
                # temp = []
                # temp.append(g.latlng[0] + random.uniform(-0.001,0.001) + 5.7525)
                # temp.append(g.latlng[1] + random.uniform(-0.001,0.001) + 4.2559)
                print((g.latlng[0] + random.uniform(-0.001,0.001) + 5.7525))
                print(g.latlng[1] + random.uniform(-0.001,0.001) + 4.2559)
                print("There are", num_people, "people in the frame")
                data.append({})
                # data[len(data)-1]['lat'] = 30.6 + random.uniform(-0.001,0.001)
                # data[len(data)-1]['long'] = -96.34 + random.uniform(-0.001,0.001)
                data[len(data)-1]['lat'] = g.latlng[0] + random.uniform(-0.001,0.001) - 1.7302
                data[len(data)-1]['long'] = g.latlng[1] + random.uniform(-0.001,0.001) + 4.3348
                data[len(data)-1]['text'] = str(num_people)
                data[len(data)-1]['message'] = image_caption

            # Display the resulting frame.
            cv2.imshow('Frame',frame)
            cv2.rectangle(cur_frame, (0, 10), (0+1750, 10+55), (255, 255, 255), -1)
            cv2.putText(cur_frame, image_caption, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), thickness=1,lineType=cv2.LINE_AA)
            if frame_num % frame_increment == 0:
                cv2.imshow("Cur_Frame",cur_frame)
            # Press Q on keyboard to  exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
            frame_num += 1

        else:
            break
    capture.release()
    cv2.destroyAllWindows()

    return data