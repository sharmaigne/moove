import streamlit as st
import cv2
import mediapipe as mp
import numpy as np

# Set up the page config and title
st.set_page_config(page_title="Tempo", layout="wide")
st.title("Tempo Fitness Rep Tracker")

# Initialize 'Settings' in session_state if not already present
if "Settings" not in st.session_state:
    st.session_state.Settings = {"Start Webcam": False}

# Sidebar controls
st.sidebar.title("Settings")
run = st.sidebar.checkbox("Start Webcam", value=False)  # Use checkbox for webcam toggle

# Update session_state when checkbox is toggled
st.session_state.Settings["Start Webcam"] = run

# Initialize MediaPipe Pose
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

frame_placeholder = st.empty()  # Placeholder for video stream

# Start video stream
if run:
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            st.warning("Unable to access camera.")
            break

        # Flip frame for mirror view
        frame = cv2.flip(frame, 1)

        # Convert to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb_frame)

        # Draw landmarks
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                frame,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=3),
                mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2)
            )

        frame_placeholder.image(frame, channels="BGR")

        # Break when user stops the toggle
        if not st.session_state.Settings["Start Webcam"]:
            break

    cap.release()
