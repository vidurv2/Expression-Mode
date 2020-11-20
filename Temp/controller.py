import os
import requests
from Temp import constants
import cv2
import time
import shutil


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
        headers = {'Content-Type': 'application/octet-stream',
                   'Ocp-Apim-Subscription-Key': subscription_key}
        params = {
            'detectionModel': 'detection_01',
            'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
            'returnFaceId': 'true'
        }

        # API Call
        response = requests.post(face_api_url, params=params,
                                 headers=headers, data=image_url)
        response.raise_for_status()
        return response.json()

    def outputDisplay(self, result):
        # Vidur's Code
        pass

    def main(self, video_dir, output_dir, frame_rate):
        # Creating a VideoCapture object to read the video
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        cap = cv2.VideoCapture(video_dir)
        ticks = time.time()
        i = 0
        # Loop until the end of the video
        while cap.isOpened():
            # Capture frame-by-frame
            ret, frame = cap.read()
            frame = cv2.resize(frame, (1920, 1080), fx=0, fy=0,
                               interpolation=cv2.INTER_CUBIC)

            # Display the resulting frame

            if (time.time() - ticks) > frame_rate and ret:
                ticks = time.time()
                # cv2.imshow('Frame', frame)

                cv2.imwrite(os.path.join(
                    output_dir, 'img' + '.jpg'), frame)
                i += 1
                # API Call
                data = open('frames/img.jpg', 'rb')
                output = self.apiCall(
                    image_url=data)
                print(output)
                print("------------------------------")

                # self.outputDisplay(output)

            # conversion of BGR to grayscale is necessary to apply this operation
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Output Display

            # adaptive thresholding to use different threshold
            # values on different regions of the frame.
            Thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                           cv2.THRESH_BINARY_INV, 11, 2)

            # cv2.imshow('Thresh', Thresh)
            # define q as the exit button
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        # if cv2.waitKey(25) & 0xFF == ord('q'):
        #     break

        # release the video capture object
        cap.release()
        # Closes all the windows currently opened.
        cv2.destroyAllWindows()
        shutil.rmtree("frames")
