import cv2

class Visualizer():
    def __init__(self):
        pass

    def draw_count(self, frame, count):

        w, h, _ = frame.shape

        # Rectangle dimensions (top-left corner, 1/5 width and 1/10 height)
        x1, y1 = 0, 0
        x2, y2 = w // 3, h // 8

        text = f"Push ups: {count}"

        frame = cv2.rectangle(frame,(x1, y1), (x2, y2),(0,165,255), -1)
        
        # Adjust fontSize so it fits
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 2
        thickness = 2

        (text_w, text_h), baseline = cv2.getTextSize(text, font, font_scale, thickness)

        # Shrink font scale if text is too wide
        while text_w > (x2 - x1 - 10):  # padding of 10 px
            font_scale -= 0.1
            (text_w, text_h), baseline = cv2.getTextSize(text, font, font_scale, thickness)

        # Center text inside rectangle
        text_x = x1 + (x2 - x1 - text_w) // 2
        text_y = y1 + (y2 - y1 + text_h) // 2

        # Put text (black)
        frame = cv2.putText(frame, text, (text_x, text_y), font,
                            font_scale, (0, 0, 0), thickness, cv2.LINE_AA)

        return frame