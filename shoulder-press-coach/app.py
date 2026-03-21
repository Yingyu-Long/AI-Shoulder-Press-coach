"""Main entry point for the shoulder press coaching app."""

from __future__ import annotations

import cv2

from src.detector.exercise_detector import ShoulderPressDetector
from src.detector.pose_detector import PoseDetector
from src.logic.feedback import generate_feedback
from src.logic.rep_counter import RepCounter
from src.utils.drawing import (
    draw_angle_label,
    draw_header,
    draw_pose_landmarks,
)


def main() -> None:
    """Start the webcam loop and run the shoulder press coach."""
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Could not open webcam. Check camera permissions and device access.")

    pose_detector = PoseDetector()
    exercise_detector = ShoulderPressDetector(side="right")
    rep_counter = RepCounter()

    try:
        while True:
            success, frame = cap.read()
            if not success:
                print("Warning: failed to read a frame from the webcam.")
                break

            frame = cv2.flip(frame, 1)
            pose_result = pose_detector.process(frame)

            metrics = None
            stage = rep_counter.stage
            rep_count = rep_counter.reps
            feedback_text = "Get in frame"

            if pose_result.landmarks:
                metrics = exercise_detector.analyze(pose_result.landmarks, frame.shape)
                stage, rep_count, rep_event = rep_counter.update(metrics)
                feedback_text = generate_feedback(metrics, stage, rep_event)
                draw_pose_landmarks(frame, pose_result, pose_detector.pose_connections)
            else:
                rep_event = None

            draw_header(frame, rep_count, stage, feedback_text)

            if metrics and metrics.elbow_point:
                draw_angle_label(frame, metrics.elbow_point, metrics.elbow_angle)

            cv2.imshow("Shoulder Press Coach", frame)

            key = cv2.waitKey(1) & 0xFF
            if key in (27, ord("q")):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
        pose_detector.close()


if __name__ == "__main__":
    main()
