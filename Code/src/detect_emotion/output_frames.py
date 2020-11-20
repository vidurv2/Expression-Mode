from bounding_box import bounding_box as bb
from constants import EMOTION_TXT_FILE, RAW_FRAMES_OUTPUT_DIR, EMOJI_IMAGES_PATH, RESULT_FRAMES_PATH
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

LEFT_EMOJI = (145, 770)
TOP_RIGHT_EMOJI = (980, 370)
BOTTOM_RIGHT_EMOJI = (980, 770)

BOTTOM_BOXES = 900
LEFT_BOX = 800
TOP_RIGHT_BOX = 500


def make_box():

    with open(EMOTION_TXT_FILE, 'r') as eFile:
        lines = eFile.readlines()
        for i, row in enumerate(lines):
            frame = json.loads(row)

            path = RAW_FRAMES_OUTPUT_DIR + '/img' + str(i) + '.jpg'
            image = cv2.imread(path, cv2.IMREAD_COLOR)

            for face in frame:

                box = face["faceRectangle"]

                # Remove the bottom box
                if box["top"] > BOTTOM_BOXES:
                    continue

                emotion = calc_max_emotion(face["faceAttributes"]["emotion"])

                # Make Box
                bb.add(image, box['left'], box['top'], box['left'] + box['width'], box['top'] + box['height'], emotion, EMOTION_COLOR_DICT[emotion])

                # Add emoji
                overlay = cv2.imread(EMOJI_IMAGES_PATH + '\\' + emotion + '.png')
                rows, cols, channels = overlay.shape

                # Finding emoji loc

                if box['left'] < LEFT_BOX:
                    emoji_coods = LEFT_EMOJI

                elif box['top'] < TOP_RIGHT_BOX:
                    emoji_coods = TOP_RIGHT_EMOJI

                else:
                    emoji_coods = BOTTOM_RIGHT_EMOJI

                overlay = cv2.addWeighted(image[emoji_coods[1]:emoji_coods[1] + rows, emoji_coods[0]:emoji_coods[0] + cols], 0.2, overlay, 0.8, 0)

                image[emoji_coods[1]:emoji_coods[1] + rows, emoji_coods[0]:emoji_coods[0] + cols] = overlay

            cv2.imwrite(RESULT_FRAMES_PATH + '/img' + str(i) + '.png', image)


def calc_max_emotion(emotions):
    emotion, max_emotion_val = "anger", 0
    for e, e_value in emotions.items():
        if max_emotion_val < e_value:
            emotion = e
            max_emotion_val = e_value
    return emotion


