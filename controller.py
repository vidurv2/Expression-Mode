import json
import os
import requests
import constants


class Controller:
    def __init__(self):
        self.subscription_key = constants.FACE_SUBSCRIPTION_KEY
        self.endpoint = constants.FACE_ENDPOINT

    def apiCall(self, image_url):
        # API Auth
        subscription_key = self.subscription_key
        assert subscription_key
        face_api_url = self.endpoint + '/face/v1.0/detect'

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
                                 headers=headers, json={"url": image_url})

        # Response
        return json.dumps(response.json())

    def outputDisplay(self, output):
        # Vidur's Code
        pass

    def inputConfig(self):
        # Ritwik's Code
        pass
