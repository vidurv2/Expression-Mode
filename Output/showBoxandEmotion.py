import numpy as np
from cv2 import cv2
import json
import operator

#Read json to create dictionary 
with open('test-result.json','r') as f:
    result = json.load(f)

#Import frame
num_faces = len(result)
img = cv2.imread("test_img.jpeg",1)

for i in range(num_faces):
    #Draw bounding boxes 
    start_x = result[i]["faceRectangle"]["left"]
    start_y = result[i]["faceRectangle"]["top"]
    end_x = start_x + result[i]["faceRectangle"]["width"]
    end_y = start_y + result[i]["faceRectangle"]["height"]
    cv2.rectangle(img,(start_x,start_y),(end_x,end_y),(255,0,0))
    
    #Display emotion with highest score 
    emotions_dict = result[i]["faceAttributes"]["emotion"]
    highest_emotion = max(emotions_dict.items(),key=operator.itemgetter(1))[0]
    cv2.putText(img , highest_emotion,(start_x-5,start_y-5),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255), 2)
    

cv2.imshow("Image",img)
cv2.moveWindow("Image",0,0)

cv2.waitKey(0)
cv2.destroyAllWindows()
