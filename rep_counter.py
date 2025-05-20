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
        requirement = 0.005  # Sensitivity for squat depth

        # Get Y-coordinates of key points
        left_knee = landmarks.landmark[LANDMARKS["left_knee"]].y
        right_knee = landmarks.landmark[LANDMARKS["right_knee"]].y
        left_hip = landmarks.landmark[LANDMARKS["left_hip"]].y
        right_hip = landmarks.landmark[LANDMARKS["right_hip"]].y

        # Average positions
        knee_avg = (left_knee + right_knee) / 2
        hip_avg = (left_hip + right_hip) / 2

        if not self.in_progress and knee_avg > hip_avg + requirement:
            # Squatting down - knees are clearly below hips
            self.in_progress = True

        elif self.in_progress and knee_avg < hip_avg - requirement:
            # Standing up - knees are clearly above hips
            self.rep_count += 1
            self.in_progress = False

        return self.rep_count, self.in_progress

    def _update_jumping_jacks(self, landmarks):
        """
        Logic to count jumping jacks based on pose landmarks.
        """

        if not landmarks:
            return self.rep_count, self.in_progress

        left_wrist = landmarks.landmark[LANDMARKS["left_wrist"]]
        right_wrist = landmarks.landmark[LANDMARKS["right_wrist"]]
        left_shoulder = landmarks.landmark[LANDMARKS["left_shoulder"]]
        right_shoulder = landmarks.landmark[LANDMARKS["right_shoulder"]]
        left_ankle = landmarks.landmark[LANDMARKS["left_ankle"]]
        right_ankle = landmarks.landmark[LANDMARKS["right_ankle"]]

        # Arms up if both wrists are higher than shoulders by a margin
        arms_up = (
            left_wrist.y < left_shoulder.y - 0.1
            and right_wrist.y < right_shoulder.y - 0.1
        )

        # Arms down if both wrists are near or below shoulders
        arms_down = (
            left_wrist.y > left_shoulder.y
            and right_wrist.y > right_shoulder.y
        )

        # Compute horizontal distance between ankles
        ankle_distance = abs(left_ankle.x - right_ankle.x)

        # Estimate shoulder width to normalize distance (optional)
        shoulder_width = abs(left_shoulder.x - right_shoulder.x)

        # Legs spread if ankle distance > 1.2 * shoulder width (adjust factor)
        legs_spread = ankle_distance > shoulder_width * 1.2

        # Legs together if ankle distance < shoulder width * 0.8 (adjust factor)
        legs_together = ankle_distance < shoulder_width * 0.8

        # Detect jumping jack open position
        jumping_jack_open = arms_up and legs_spread

        # Detect jumping jack closed position
        jumping_jack_closed = arms_down and legs_together

        if jumping_jack_open and not self.in_progress:
            self.in_progress = True

        elif jumping_jack_closed and self.in_progress:
            self.rep_count += 1
            self.in_progress = False

        return self.rep_count, self.in_progress


