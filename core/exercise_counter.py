
class ExcerciseCounter():
    def __init__(self):
        self.count = 0 
        self.stage = None

    def update(self, landmarks):
        """Update counter based on landmarks (to be implemented in subclass)."""
        raise NotImplementedError