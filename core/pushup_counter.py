from .exercise_counter import ExcerciseCounter

class PushUpCounter(ExcerciseCounter):
    def __init__(self):
        pass

    def update(self):
        pass

    def classify_up_down(self, frame, landmarks):
        state = "other"
        
        # selection left right by visibility

        # return "up", "down", "other"

        pass