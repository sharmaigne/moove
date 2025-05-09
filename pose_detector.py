from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import mediapipe as mp
import cv2
from mediapipe.python.solutions.drawing_utils import DrawingSpec

# MediaPipe Pose setup
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# Exclude facial landmarks (indices 0–10)
LAST_FACE_LANDMARK = 10

# Filter out face-related connections
BODY_CONNECTIONS = [
    (a, b)
    for (a, b) in mp_pose.POSE_CONNECTIONS
    if a > LAST_FACE_LANDMARK or b > LAST_FACE_LANDMARK
]

# Custom landmark drawing style
LANDMARK_STYLE = {
    i: DrawingSpec(color=(0, 155, 0), thickness=2, circle_radius=2) for i in range(33)
}
for i in range(LAST_FACE_LANDMARK + 1):
    LANDMARK_STYLE[i] = DrawingSpec(color=(255, 255, 0), thickness=0, circle_radius=0)


def draw_landmarks(img, landmarks):
    mp_drawing.draw_landmarks(
        img,
        landmarks,
        BODY_CONNECTIONS,
        landmark_drawing_spec=LANDMARK_STYLE,
        connection_drawing_spec=DrawingSpec(color=(200, 0, 155), thickness=2),
    )


def process_frame(frame):
    img = frame.to_ndarray(format="rgb24")
    # flip the image horizontally for a mirror effect
    img = cv2.flip(img, 1)
    results = pose.process(img)

    return results, img
