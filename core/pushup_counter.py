import numpy as np

from .exercise_counter import ExcerciseCounter

# Landmark indices
LEFT_SHOULDER = 11
RIGHT_SHOULDER = 12
LEFT_ELBOW = 13
RIGHT_ELBOW = 14
LEFT_WRIST = 15
RIGHT_WRIST = 16


class PushUpCounter(ExcerciseCounter):
    def __init__(self):
        super().__init__() 
        self.stage = "other"
        self.stage_sequence = []

    def update(self, landmarks, method="ml"):

        if method=="ml":
            self.classify_up_down(landmarks) # updates self.stage
        elif method=="logic":
            self.classify_up_down_logic(landmarks) # updates self.stage

        # Only append if stage changes
        if not self.stage_sequence or self.stage != self.stage_sequence[-1]:
            self.stage_sequence.append(self.stage)

        # remove "other" from sequence
        filtered = [s for s in self.stage_sequence if s != "other"]

        if len(filtered) >= 3 and filtered[-3:] == ["up", "down", "up"]:
            self.count += 1
            self.stage_sequence = []  # reset after counting 
        
        return self.count, self.stage


    def classify_up_down_logic(self, landmarks):
        
        # Extract landmarks
        left_shoulder = landmarks[LEFT_SHOULDER]
        right_shoulder = landmarks[RIGHT_SHOULDER]
        left_elbow = landmarks[LEFT_ELBOW]
        right_elbow = landmarks[RIGHT_ELBOW]
        left_wrist = landmarks[LEFT_WRIST]
        right_wrist = landmarks[RIGHT_WRIST]

        # Determine left or right view
        if np.mean([left_shoulder.visibility, left_elbow.visibility]) > 0.5 and np.mean([left_shoulder.visibility, left_elbow.visibility]) > np.mean([right_shoulder.visibility, right_elbow.visibility]):
            view = "left"
        elif np.mean([right_shoulder.visibility, right_elbow.visibility]) > 0.5:
            view = "right"
        else:
            view = None
            position = "other"

        if view == "left":
            position = self.position_schoulder_elbow(left_shoulder, left_elbow)
        if view == "right":
            position = self.position_schoulder_elbow(right_shoulder, right_elbow)

        self.stage = position

    def position_schoulder_elbow(self, shoulder, elbow):
        if shoulder.y < elbow.y:
            position = "up"
        elif shoulder.y > elbow.y:
            position = "down"
        else:
            position = "other"
        return position


    def classify_up_down(self, landmarks):
        
        # selection left right by visibility

        # return "up", "down", "other"

        if self.stage == "other":
            self.stage = "up"
        elif self.stage == "up":
            self.stage = "down"
        elif self.stage == "down":
            self.stage = "up"
