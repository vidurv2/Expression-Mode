from bounding_box import bounding_box as bb
from constants import EMOTION_CSV_FILE, RAW_FRAMES_OUTPUT_DIR, EMOJI_IMAGES_PATH, RESULT_FRAMES_PATH
import cv2
import csv
import json

EMOTION_COLOR_DICT = {
    'anger': 'red',
    'contempt': 'black',
    'disgust': 'orange',
    'fear': 'blue',
    'happiness': 'green',
    'neutral': 'yellow',
    'sadness': 'red',
    'surprise': 'blue'
}


def make_box():

    with open(EMOTION_CSV_FILE, 'r') as csvFile:
        reader = csv.reader(csvFile)
        for i, row in enumerate(reader):
            if i == 0:
                continue
            path = RAW_FRAMES_OUTPUT_DIR + '/img' + str(row[0]) + '.jpg'
            image = cv2.imread(path, cv2.IMREAD_COLOR)
            row[1] = row[1].replace("\'", "\"")
            box = json.loads(row[1])
            emotion = row[2]

            # Make Box
            bb.add(image, box['left'], box['top'], box['left'] + box['width'], box['top'] + box['height'], emotion,
                   EMOTION_COLOR_DICT[emotion])

            # Add emoji
            overlay = cv2.imread( EMOJI_IMAGES_PATH + '\\' + emotion + '.png')
            rows, cols, channels = overlay.shape
            overlay = cv2.addWeighted(image[250:250 + rows, 0:0 + cols], 0, overlay, 1, 0)
            image[-rows:, 0:0 + cols] = overlay
            cv2.imwrite(RESULT_FRAMES_PATH + '/img' + row[0] + '.png', image)
