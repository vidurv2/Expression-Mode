from src.detect_emotion import generate_frames, api_call, output_frames, combine_frames

FRAME_RATE = 0.2
FPS = 10

# Generate Frames
num_frames = generate_frames.generate_frames(frame_rate=FRAME_RATE)

# Make the API call and store response in txt file
api_call.storeToFile(num_frames)

# Make the bounding box and overlay emoji
output_frames.make_box()

# Combine frames to make video
combine_frames.make_video(num_frames, fps=FPS)
