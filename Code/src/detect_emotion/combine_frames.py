import cv2
from constants import RESULT_FRAMES_PATH, DATA_DIR


def make_video(num_frames, fps):

    print('Combining Frames...')
    img_array = []
    for i in range(num_frames):
        img = cv2.imread(RESULT_FRAMES_PATH + '/img' + str(i) + '.png')
        height, width, layers = img.shape
        size = (width, height)
        img_array.append(img)

    out = cv2.VideoWriter(DATA_DIR + '/result_video.avi', cv2.VideoWriter_fourcc(*'DIVX'), fps, size)

    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()
    print('Combining Frames: FINISHED')
    print('----------------------------------------')
    print('Result Video in:' + DATA_DIR)
