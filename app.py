import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import cv2
import av

from pose_detector import *

st.set_page_config(page_title="Tempo", layout="wide")
st.title("Tempo Fitness Rep Tracker")

# Main Video Processor
class PoseDetector(VideoProcessorBase):
    def recv(self, frame):
        results, img = process_frame(frame)
        if results.pose_landmarks:
            draw_landmarks(img, results.pose_landmarks)

        return av.VideoFrame.from_ndarray(img, format="rgb24")


# Start webcam stream
webrtc_streamer(
    key="pose",
    video_transformer_factory=PoseDetector,
    media_stream_constraints={"video": True, "audio": False},
)
