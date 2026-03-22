"""Main entry point for the shoulder press coaching app."""

from __future__ import annotations
import cv2
import time

from src.config import DEFAULT_REP_GOAL
from src.detector.exercise_detector import ShoulderPressDetector
from src.detector.pose_detector import PoseDetector
from src.logic.rep_counter import RepCounter
from src.utils.drawing import (
    draw_angle_label,
    draw_header,
    draw_pose_landmarks,
    draw_correction_feedback,
    draw_completion_animation,
)

def prompt_rep_goal() -> int:
    """Prompt the user for today's rep goal."""
    raw_value = input(f"How much do you wanna press today? [{DEFAULT_REP_GOAL}]: ").strip()
    if not raw_value:
        return DEFAULT_REP_GOAL

    try:
        rep_goal = int(raw_value)
    except ValueError:
        print(f"Invalid input. Using default goal of {DEFAULT_REP_GOAL}.")
        return DEFAULT_REP_GOAL

    if rep_goal <= 0:
        print(f"Goal must be positive. Using default goal of {DEFAULT_REP_GOAL}.")
        return DEFAULT_REP_GOAL

    return rep_goal

def main() -> None:
    """Start the webcam loop and run the shoulder press coach."""
    rep_goal = prompt_rep_goal()

    completion_animation_start = None
    animation_duration = 3.0  # seconds
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Could not open webcam. Check camera permissions and device access.")

    pose_detector = PoseDetector()
    exercise_detector = ShoulderPressDetector(side="right")
    rep_counter = RepCounter(rep_goal=rep_goal)

    
    try:
        while True:
            success, frame = cap.read()
            if not success:
                print("Warning: failed to read a frame from the webcam.")
                break

            current_time = time.time()
            frame = cv2.flip(frame, 1)
            pose_result = pose_detector.process(frame)

            metrics = None
            is_correct = True
            
            # Default UI state before person enters frame
            stage = "Unknown"
            breath = "-"
            rep_count = rep_counter.reps
            feedback_text = "Please step into the frame"

            if pose_result.landmarks:
                metrics = exercise_detector.analyze(pose_result.landmarks, frame.shape)
                
                # The state machine now returns all necessary UI data
                state = rep_counter.update(metrics, current_time)
                
                stage = state.frontend_stage
                breath = state.breath
                feedback_text = state.feedback
                is_correct = state.is_correct
                rep_count = state.reps

                draw_pose_landmarks(frame, pose_result, pose_detector.pose_connections, is_correct)

                # NEW: Draw the correction arrow if form is bad
                if not state.is_correct:
                    draw_correction_feedback(frame, metrics)
            draw_header(frame, rep_count, rep_goal, stage, breath, feedback_text, is_correct)

            if metrics and metrics.visibility_ok:
                draw_angle_label(frame, metrics.elbow_point, metrics.elbow_angle, is_correct)
            
            if rep_count >= rep_goal and completion_animation_start is None:
                completion_animation_start = current_time

            if completion_animation_start is not None:
                animation_elapsed = current_time - completion_animation_start
                if animation_elapsed <= animation_duration:
                    draw_completion_animation(frame, animation_elapsed, rep_goal)

            cv2.imshow("Shoulder Press Coach", frame)

            key = cv2.waitKey(1) & 0xFF
            if key in (27, ord("q")):
                break
            if key in (ord("r"), ord("R")):
                rep_counter.reset()
                completion_animation_start = None
    finally:
        cap.release()
        cv2.destroyAllWindows()
        pose_detector.close()

if __name__ == "__main__":
    main()