from utils import LANDMARKS

class RepCounter:
    def __init__(self, exercise):
        self.exercise = exercise
        self.rep_count = 0
        self.in_progress = False  # state: e.g., squat in progress

    def update(self, landmarks):
        if self.exercise == "Squats":
            self.rep_count, self.in_progress = self._update_squats(landmarks)
        elif self.exercise == "Jumping Jacks":
            self.rep_count, self.in_progress = self._update_jumping_jacks(landmarks)

        return self.rep_count

    def get_count(self):
        return self.rep_count

    def reset(self):
        self.rep_count = 0
        self.in_progress = False

    def _update_squats(self, landmarks):
        """
        Logic to count squats based on pose landmarks.
        """
        tolerance = 0.05  # Tolerance for detecting squat completion

        # Extract relevant landmark positions using LANDMARKS dictionary
        left_knee = landmarks.landmark[LANDMARKS["left_knee"]].y
        right_knee = landmarks.landmark[LANDMARKS["right_knee"]].y
        left_hip = landmarks.landmark[LANDMARKS["left_hip"]].y
        right_hip = landmarks.landmark[LANDMARKS["right_hip"]].y

        # Check if knees are lower than hips (squatting down)
        if not self.in_progress:
            if left_knee < left_hip - tolerance and right_knee < right_hip - tolerance:
                # Start of a new squat
                self.in_progress = True

        # Check if knees are above hips (standing up)
        elif self.in_progress:
            if left_knee > left_hip + tolerance and right_knee > right_hip + tolerance:
                # End of a squat
                self.rep_count += 1
                self.in_progress = False

        return self.rep_count, self.in_progress


    def _update_jumping_jacks(self, landmarks):
        """
        Logic to count jumping jacks based on pose landmarks.
        """

        tolerance = 0.05  # Tolerance for detecting a full rep (arms and legs spread)

        if landmarks:
            # Extract relevant landmark positions
            left_shoulder = landmarks.landmark[LANDMARKS["left_shoulder"]].y
            right_shoulder = landmarks.landmark[LANDMARKS["right_shoulder"]].y
            left_hip = landmarks.landmark[LANDMARKS["left_hip"]].y
            right_hip = landmarks.landmark[LANDMARKS["right_hip"]].y
            left_ankle = landmarks.landmark[LANDMARKS["left_ankle"]].y
            right_ankle = landmarks.landmark[LANDMARKS["right_ankle"]].y

            # Check if arms are overhead and legs are spread (jumping jack position)
            if (
                left_shoulder.y < 0.4
                and right_shoulder.y < 0.4
                and left_hip.y < 0.4
                and right_hip.y < 0.4
                and left_ankle.y < 0.6
                and right_ankle.y < 0.6
            ):
                if not self.in_progress:
                    # Start of a new jumping jack rep
                    self.in_progress = True

            # Check if arms are back at sides and legs are together
            elif (
                left_shoulder.y > 0.7
                and right_shoulder.y > 0.7
                and left_hip.y > 0.7
                and right_hip.y > 0.7
                and left_ankle.y > 0.8
                and right_ankle.y > 0.8
            ):
                if self.in_progress:
                    # End of a jumping jack rep
                    self.rep_count += 1
                    self.in_progress = False

        return self.rep_count, self.in_progress

