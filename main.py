import cv2

from core.video_handler import VideoHandler
from core.pose_detector import PoseDetector
from core.pushup_counter import PushUpCounter
from core.visualizer import Visualizer


def main():

    # Initiate video, detector, counter and visualizer
    video = VideoHandler(source=0) # 0 default webcam
    detector = PoseDetector()
    counter = PushUpCounter()
    visualizer = Visualizer()

    while video.is_open():
        frame = video.get_frame()
        if frame is None:
            break

        
        results = detector.detect(frame) # media pipe pose detection

        if results.pose_landmarks:
            count, stage = counter.update(results.pose_landmarks.landmark, method="logic")
            #count = 100
            frame = detector.draw(frame, results)
            frame = visualizer.draw_count(frame, count)
            frame = visualizer.draw_stage(frame, stage)           

        video.show(frame)

        if video.should_quit('q'):
            break

    video.release()


if __name__ == "__main__":
    main()
