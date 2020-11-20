from cv2 import cv2
import numpy as np
import json
import operator
import json
import os
import requests
import cv2
import time

FACE_SUBSCRIPTION_KEY = '6ae7a9af9b4245dda0ee29fc83ecb28c'
FACE_ENDPOINT = 'https://videorecognition.cognitiveservices.azure.com/'

output_dir = 'frames'
frame_rate = 3

# Capture video
cap = cv2.VideoCapture("/Users/jay/Desktop/sample.mp4")

while True:
    # Grab a single frame of the video
    ret, frame = cap.read()

    frame = cv2.resize(frame, (1920, 1080), fx=0, fy=0,
                       interpolation=cv2.INTER_CUBIC)

    # Display the resulting frame
    ticks = time.time()
    if (time.time() - ticks) > frame_rate and ret:
        ticks = time.time()
        # cv2.imshow('Frame', frame)

        cv2.imwrite(os.path.join(
            output_dir, 'img' + '.jpg'), frame)

        # API Call

        subscription_key = FACE_SUBSCRIPTION_KEY
        assert subscription_key
        face_api_url = FACE_ENDPOINT + '/face/v1.0/detect'

        # API Config
        # image_url = 'https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/ComputerVision/Images/faces.jpg'
        headers = {'Ocp-Apim-Subscription-Key': subscription_key}
        params = {
            'detectionModel': 'detection_01',
            'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
            'returnFaceId': 'true'
        }

        # API Call
        response = requests.post(face_api_url, params=params,
                                 headers=headers, json={"url": "http://0.0.0.0:8000/test_img.jpeg"})

        # Response
        output = json.dumps(response.json())

    # Call API on frame to generate json
    result = output

    # Number of faces detected in current frame of video
    num_faces = len(result)

    for i in range(num_faces):
        # Draw bounding box of each face
        start_x = result[i]["faceRectangle"]["left"]
        start_y = result[i]["faceRectangle"]["top"]
        end_x = start_x + result[i]["faceRectangle"]["width"]
        end_y = start_y + result[i]["faceRectangle"]["height"]
        cv2.rectangle(frame, (start_x, start_y),
                      (end_x, end_y), (0, 0, 255), 2)

        # Display emotion with highest score of each face
        emotions_dict = result[i]["faceAttributes"]["emotion"]
        highest_emotion = max(emotions_dict.items(),
                              key=operator.itemgetter(1))[0]
        cv2.rectangle(frame, (start_x, end_y), (end_x, end_y+25),
                      (0, 0, 255), cv2.FILLED)
        cv2.putText(frame, highest_emotion, (start_x, end_y+13),
                    cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)

    # Show the output
    cv2.imshow("Video", frame)

    # Terminate program when "q" key is pressed
    ch = cv2.waitKey(1)
    if ch & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()
