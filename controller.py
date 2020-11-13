import json
import os
import requests
import constants
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
        headers = {'Ocp-Apim-Subscription-Key': subscription_key}
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
        num_faces = len(result)
        img = cv2.imread("Output Display/test_img.jpeg", 1)
        for i in range(num_faces):
            start_x = result[i]["faceRectangle"]["left"]
            start_y = result[i]["faceRectangle"]["top"]
            end_x = start_x + result[i]["faceRectangle"]["width"]
            end_y = start_y + result[i]["faceRectangle"]["height"]
            cv2.rectangle(img, (start_x, start_y),
                          (end_x, end_y), (0, 0, 255), 2)
            emotions_dict = result[i]["faceAttributes"]["emotion"]
            highest_emotion = max(emotions_dict.items(),
                                  key=operator.itemgetter(1))[0]
            cv2.rectangle(img, (start_x, end_y), (end_x, end_y+25),
                          (0, 0, 255), cv2.FILLED)
            cv2.putText(img, highest_emotion, (start_x, end_y+13),
                        cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)
            # cv2.putText(img , highest_emotion,(start_x-5,start_y-5),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255), 2)

        cv2.imshow("Image", img)
        cv2.moveWindow("Image", 0, 0)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def inputConfig(self, video_dir, output_dir, frame_rate):
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
