import cv2
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np


def mpg_to_html5video(mpg_file):
    # OpenCV Video Capture
    cap = cv2.VideoCapture(mpg_file)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    frames = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frames.append(frame)
    cap.release()

    # Matplotlib Animation
    fig, ax = plt.subplots()
    ax.set_xticks([])
    ax.set_yticks([])
    im = ax.imshow(
        np.zeros((height, width, 3), dtype=np.uint8)
    )  # initial empty image

    def update(frame):
        im.set_array(frames[frame])
        return [im]

    ani = animation.FuncAnimation(
        fig, update, frames=len(frames), interval=1000 / fps
    )

    return ani.to_html5_video()
