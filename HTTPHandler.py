import json
import os
import requests
import constants

# API Auth
subscription_key = constants.FACE_SUBSCRIPTION_KEY
assert subscription_key
face_api_url = constants.FACE_ENDPOINT + '/face/v1.0/detect'

# API Config
image_url = 'https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/ComputerVision/Images/faces.jpg'
headers = {'Ocp-Apim-Subscription-Key': subscription_key}
params = {
    'detectionModel': 'detection_01',
    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
    'returnFaceId': 'true'
}

# API Call
response = requests.post(face_api_url, params=params,
                         headers=headers, json={"url": image_url})

# Response
print(json.dumps(response.json()))
