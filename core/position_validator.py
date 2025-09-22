# Landmark indices
LEFT_SHOULDER = 11
RIGHT_SHOULDER = 12
LEFT_ELBOW = 13
RIGHT_ELBOW = 14
LEFT_WRIST = 15
RIGHT_WRIST = 16
LEFT_FOOT = 29
RIGHT_FOOT = 30


class PositionValidator:
    def __init__(self):
        self.ready = False

    def check_start_position(self, landmarks):

        # Extract landmarks
        left_shoulder = landmarks[LEFT_SHOULDER]
        right_shoulder = landmarks[RIGHT_SHOULDER]
        left_elbow = landmarks[LEFT_ELBOW]
        right_elbow = landmarks[RIGHT_ELBOW]
        left_wrist = landmarks[LEFT_WRIST]
        right_wrist = landmarks[RIGHT_WRIST]
        left_foot = landmarks[LEFT_FOOT]
        right_foot = landmarks[RIGHT_FOOT]

        # Left or right side at least 0.5 visibility
        view = None
        if left_shoulder.visibility > 0.5 and left_wrist.visibility > 0.5 and left_foot.visibility > 0.5:
            view = "left"
        elif right_shoulder.visibility > 0.5 and right_wrist.visibility > 0.5 and right_foot.visibility > 0.5:
            view = "right"
        else: 
            return False

        # Schoulders above hands
        position_shoulder = "other"
        if view == "left":
            position_shoulder = self.position_schoulder_elbow(left_shoulder, left_elbow)
        elif view == "right":
            position_shoulder = self.position_schoulder_elbow(right_shoulder, right_elbow)
        if position_shoulder != "up":
            return False

        # Feets roughly horizontal with hands (same y, whitin some range) 
        position_feet = "other"
        if view == "left":
            position_feet = self.position_feet(left_foot, left_wrist)
        elif view == "right":
            position_feet = self.position_feet(right_foot, right_wrist)
        if position_feet != "horizontal":
            return False
        
        return True
    
    def position_feet(self, foot, wrist):
        if abs(foot.y - wrist.y) < 0.2:
            return "horizontal"
        return False

    def position_schoulder_elbow(self, shoulder, elbow):
        if shoulder.y < elbow.y:
            position = "up"
        elif shoulder.y > elbow.y:
            position = "down"
        else:
            position = "other"
        return position
