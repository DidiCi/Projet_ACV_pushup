import cv2

from core.video_handler import VideoHandler
from core.pose_detector import PoseDetector
from core.pushup_counter import PushUpCounter
from core.visualizer import Visualizer
from core.position_validator import PositionValidator


def main():

    # Initiate video, detector, counter and visualizer
    video = VideoHandler(source=0) # 0 default webcam
    detector = PoseDetector()
    counter = PushUpCounter()
    visualizer = Visualizer()
    validator = PositionValidator()

    # Initialize count and stage
    count, stage = 0, "other"
    start_ready = False # Not correct starting position
    valid_position = False # Valid position during push ups

    while video.is_open():
        frame = video.get_frame()
        if frame is None:
            break
        
        results = detector.detect(frame) # media pipe pose detection

        if not results.pose_landmarks: 
            if not start_ready: # Not started yet and nobody in view
               pushup_start_img = cv2.imread("assets/images/pushup_standard.png")
               frame = visualizer.draw_position_warning(frame, pushup_start_img, text=True)
            else: # No landmarks but already counted (e.g. person comes back to see score)
                frame = visualizer.draw_position_warning(frame, pushup_start_img, text=False)
                frame = visualizer.draw_count(frame, count)
                frame = visualizer.draw_stage(frame, stage)  

        elif results.pose_landmarks: # Person detected

            if not start_ready:
                start_ready = validator.check_start_position(results.pose_landmarks.landmark)
                if not start_ready:
                    frame = visualizer.draw_position_warning(frame)
                else:
                    print("✅ Starting position confirmed. Begin counting!")
            
            else: # ready for counting!
                valid_position = validator.check_position(results.pose_landmarks.landmark) # if position is still valid
                if valid_position:
                    count, stage = counter.update(results.pose_landmarks.landmark, method="logic")
                    frame = detector.draw(frame, results)
                else:
                    frame = detector.draw(frame, results)
                    frame = visualizer.draw_position_warning(frame, example_image=None, text=False)
            
        if start_ready: # Show count and stage
            frame = visualizer.draw_count(frame, count)
            frame = visualizer.draw_stage(frame, stage)           

        video.show(frame)

        if video.should_quit('q'):
            break

    video.release()


if __name__ == "__main__":
    main()
