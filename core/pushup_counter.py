import numpy as np
import joblib
from tensorflow.keras.models import load_model


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
        self.model = load_model("./model/mlp_pushup_model1.h5")
        self.scaler = joblib.load("./model/scaler_pushup.pkl")
        self.le = joblib.load("./model/label_encoder.pkl")

    def update(self, landmarks, method="ml"):

        if method=="ml":
            self.classify_up_down(landmarks) # updates self.stage
        elif method=="logic":
            self.classify_up_down_logic(landmarks) # updates self.stage
        elif method=="jamila":
            self.classify_up_down_jamila(landmarks) # updates self.stage

        # Only append if stage changes
        if not self.stage_sequence or self.stage != self.stage_sequence[-1]:
            self.stage_sequence.append(self.stage)

        # remove "other" from sequence
        filtered = [s for s in self.stage_sequence if s != "other"]

        if len(filtered) >= 3 and filtered[-3:] == ["up", "down", "up"]:
            self.count += 1
            self.stage_sequence = []  # reset after counting 
        
        return self.count, self.stage


    def classify_up_down_jamila(self, landmarks):
     
        # Seuils de hauteur de l'épaule (ajuster selon la caméra et la position)
        SHOULDER_LOW_THRESHOLD = 0.5   # Position "basse"
        SHOULDER_HIGH_THRESHOLD = 0.7  # Position "haute"

        # Position de l'épaule droite (Right Shoulder)
        shoulder = landmarks[RIGHT_SHOULDER]
        shoulder_y = shoulder.y

        # Logique de comptage des pompes
        stage = "other"
        print(shoulder_y)
        if shoulder_y < SHOULDER_LOW_THRESHOLD:
            stage = "down"
        if shoulder_y > SHOULDER_HIGH_THRESHOLD:
            stage = "up"

        self.stage = stage


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
        
        keypoints = np.array([[lm.x, lm.y] for lm in landmarks])
        X_new = keypoints.flatten().reshape(1, -1)
        X_new_scaled = self.scaler.transform(X_new)

        y_pred = self.model.predict(X_new_scaled)
        pred_class_idx = y_pred.argmax()  
        pred_label = self.le.inverse_transform([pred_class_idx])[0]

        self.stage = pred_label
