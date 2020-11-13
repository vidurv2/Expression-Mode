from cv2 import cv2 
import numpy as np
import json 
import operator 

#Capture video 
cap = cv2.VideoCapture("file_path")

while True :
    # Grab a single frame of the video 
    ret , frame = cap.read()

    #Call API on frame to generate json 
    result = "api_result"

    # Number of faces detected in current frame of video
    num_faces = len(result)
 
    for i in range(num_faces):
        #Draw bounding box of each face 
        start_x = result[i]["faceRectangle"]["left"]
        start_y = result[i]["faceRectangle"]["top"]
        end_x = start_x + result[i]["faceRectangle"]["width"]
        end_y = start_y + result[i]["faceRectangle"]["height"]
        cv2.rectangle(img,(start_x,start_y),(end_x,end_y),(0,0,255),2)

        #Display emotion with highest score of each face 
        emotions_dict = result[i]["faceAttributes"]["emotion"]
        highest_emotion = max(emotions_dict.items(),key=operator.itemgetter(1))[0]
        cv2.rectangle(img,(start_x,end_y),(end_x,end_y+25),(0,0,255),cv2.FILLED)
        cv2.putText(img,highest_emotion,(start_x,end_y+13),cv2.FONT_HERSHEY_DUPLEX,0.5,(255,255,255),1)
        
    #Show the output 
    cv2.imshow("Video",frame)

    #Terminate program when "q" key is pressed
    ch = cv2.waitKey(1)
    if ch & 0xFF == ord("q"):
        break 


cap.release()
cv2.destroyAllWindows()