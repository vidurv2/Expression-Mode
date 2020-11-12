import cv2
import os
import time


def generate_frames(video_dir, output_dir, frame_rate):
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
            cv2.imshow('Frame', frame)


            cv2.imwrite(os.path.join(output_dir, 'img' + str(i) + '.jpg'), frame)
            i += 1

        # conversion of BGR to grayscale is necessary to apply this operation
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

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


generate_frames(video_dir='/Users/i537782/Desktop/sample.mp4', output_dir='frames', frame_rate=3)
