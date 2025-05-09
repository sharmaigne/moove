import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import mediapipe as mp
import cv2
import numpy as np
import av
from mediapipe.python.solutions.drawing_utils import DrawingSpec

st.set_page_config(page_title="Tempo", layout="wide")
st.title("Tempo Fitness Rep Tracker")

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


# Main Video Processor
class PoseDetector(VideoProcessorBase):
    def recv(self, frame):
        img = frame.to_ndarray(format="rgb24")
        results = pose.process(img)
        if results.pose_landmarks:
            draw_landmarks(img, results.pose_landmarks)

        # flip the image horizontally for a mirror effect
        img = cv2.flip(img, 1)
        return av.VideoFrame.from_ndarray(img, format="rgb24")


# Start webcam stream
webrtc_streamer(
    key="pose",
    video_transformer_factory=PoseDetector,
    media_stream_constraints={"video": True, "audio": False},
)
