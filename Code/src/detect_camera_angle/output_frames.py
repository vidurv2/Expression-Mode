from bounding_box import bounding_box as bb
from constants import EMOTION_CSV_FILE, RAW_FRAMES_OUTPUT_DIR, EMOJI_IMAGES_PATH, RESULT_FRAMES_PATH
import cv2
import csv
import json

UP = {'color': 'red', 'image': 'Up.png', 'label': 'Move Camera Up'}
DOWN = {'color': 'red', 'image': 'Down.png', 'label': 'Move Camera Down'}
LEFT = {'color': 'red', 'image': 'Left.png', 'label': 'Move Camera Left'}
RIGHT = {'color': 'red', 'image': 'Right.png', 'label': 'Move Camera Right'}
WRONG = {'color': 'red', 'image': 'Cross.png', 'label': 'Place your face inside the  box'}
CORRECT = {'color': 'green', 'image': 'Tick.png', 'label': 'Perfect!'}

BOX = {'left': 750, 'right': 1200, 'top': 350, 'bottom': 630}

SIGN_ROW = 740
SIGN_COL = 110


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

            if not box:
                direction = WRONG

            else:
                direction = CORRECT

                if box['top'] + box['height'] > BOX['bottom']:
                    direction = DOWN
                elif box['top'] < BOX['top']:
                    direction = UP
                elif box['left'] + box['width'] > BOX['right']:
                    direction = RIGHT
                elif box['left'] < BOX['left']:
                    direction = LEFT

                bb.add(image, BOX['left'], BOX['top'], BOX['right'], BOX['bottom'], direction['label'], direction['color'])

            # Add sign
            overlay = cv2.imread(EMOJI_IMAGES_PATH + '\\' + direction['image'])
            rows, cols, channels = overlay.shape

            overlay = cv2.addWeighted(image[SIGN_ROW:SIGN_ROW+rows, SIGN_COL:SIGN_COL + cols], 0, overlay, 0.8, 0.2)
            image[SIGN_ROW:SIGN_ROW+rows, SIGN_COL:SIGN_COL + cols] = overlay

            cv2.imwrite(RESULT_FRAMES_PATH + '/img' + row[0] + '.png', image)
