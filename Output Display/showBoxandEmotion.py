import numpy as np
from cv2 import cv2
import json
import operator

with open('Output Display/test-result.json', 'r') as f:
    result = json.load(f)

num_faces = len(result)
img = cv2.imread("Output Display/test_img.jpeg", 1)
for i in range(num_faces):
    start_x = result[i]["faceRectangle"]["left"]
    start_y = result[i]["faceRectangle"]["top"]
    end_x = start_x + result[i]["faceRectangle"]["width"]
    end_y = start_y + result[i]["faceRectangle"]["height"]
    cv2.rectangle(img, (start_x, start_y), (end_x, end_y), (0, 0, 255), 2)
    emotions_dict = result[i]["faceAttributes"]["emotion"]
    highest_emotion = max(emotions_dict.items(), key=operator.itemgetter(1))[0]
    cv2.rectangle(img, (start_x, end_y), (end_x, end_y+25),
                  (0, 0, 255), cv2.FILLED)
    cv2.putText(img, highest_emotion, (start_x, end_y+13),
                cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)
    # cv2.putText(img , highest_emotion,(start_x-5,start_y-5),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255), 2)


cv2.imshow("Image", img)
cv2.moveWindow("Image", 0, 0)

cv2.waitKey(0)
cv2.destroyAllWindows()
