# Real-Time Squat Detection using Pose Estimation

A real-time squat counter using Python, OpenCV, and MediaPipe. This project applies computer vision to detect squats based on human pose landmarks, counting repetitions with a configurable threshold to minimize false positives.

## Features

- Real-time video feed from webcam
- Pose estimation using MediaPipe
- Accurate squat detection using knee and hip landmark positions
- Repetition counting with debouncing logic
- Interactive UI with Streamlit

## Getting Started

### Prerequisites

- Python 3.8 or higher
- A functional webcam
- Stable lighting and a clear view of the user

### Installation

1. Clone this repository:

```bash
git clone https://github.com/yourusername/squat-detector
cd squat-detector
```

2. Set up a virtual environment and install dependencies:
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```
