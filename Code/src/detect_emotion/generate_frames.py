import cv2
import os
import time
from constants import VIDEO_DIR, RAW_FRAMES_OUTPUT_DIR


def generate_frames(frame_rate):

    print('Generating Frames...')
    i = 0
    try:
        # Creating a VideoCapture object to read the video
        if not os.path.exists(RAW_FRAMES_OUTPUT_DIR):
            os.mkdir(RAW_FRAMES_OUTPUT_DIR)
        cap = cv2.VideoCapture(VIDEO_DIR)
        ticks = time.time()

        # Loop until the end of the video
        while cap.isOpened():
            # Capture frame-by-frame

            ret, frame = cap.read()
            frame = cv2.resize(frame, (1920, 1080), fx=0, fy=0,
                               interpolation=cv2.INTER_CUBIC)

            # Display the resulting frame
            if (time.time() - ticks) > frame_rate and ret:
                ticks = time.time()
                cv2.imshow('Frame', frame)

                cv2.imwrite(os.path.join(RAW_FRAMES_OUTPUT_DIR, 'img'+str(i)+'.jpg'.format(i)), frame)
                i += 1

            # define q as the exit button
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        # release the video capture object
        cap.release()
        # Closes all the windows currently opened.
        cv2.destroyAllWindows()

    except cv2.error:
        pass

    num_frames = i

    print('Number of frames generated: ', num_frames)
    print('Generating Frames: FINISHED')
    print('----------------------------------------')

    return num_frames