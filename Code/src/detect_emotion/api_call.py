import requests
import csv
from time import sleep
from constants import RAW_FRAMES_OUTPUT_DIR, EMOTION_TXT_FILE, FACE_SUBSCRIPTION_KEY, FACE_ENDPOINT
import json

SLEEP_TIME = 60
MAX_FRAMES_PER_MIN = 20


def apiCall(image_path):

    # API Config
    subscription_key = FACE_SUBSCRIPTION_KEY
    face_api_url = FACE_ENDPOINT + '/face/v1.0/detect'

    # Read the image into a byte array
    image_data = open(image_path, "rb").read()
    headers = {'Ocp-Apim-Subscription-Key': subscription_key, 'Content-Type': 'application/octet-stream'}
    params = {
        'detectionModel': 'detection_01',
        'returnFaceAttributes': 'emotion',
        'returnFaceId': 'true'
    }

    # API Call
    response = requests.post(face_api_url, headers=headers, params=params, data=image_data)
    response.raise_for_status()
    return response.json()


def storeToFile(num_frames):

    with open(EMOTION_TXT_FILE, 'w') as eFile:
        iterations = num_frames
        cur_iteration = 0

        print('API calls started...')

        while iterations >= 0:
            for i in range(min(iterations, MAX_FRAMES_PER_MIN)):
                image_path = RAW_FRAMES_OUTPUT_DIR + "/img"+str(cur_iteration*20+i) + ".jpg"
                response = apiCall(image_path)
                print(response)
                eFile.write(json.dumps(response))
                eFile.write("\n")
            cur_iteration += 1
            iterations -= MAX_FRAMES_PER_MIN
            if iterations <= 0:
                break
            print('In progress... (Sleeping for 1 min)')
            sleep(SLEEP_TIME)

        print('API calls: FINISHED')
        print('----------------------------------------')
