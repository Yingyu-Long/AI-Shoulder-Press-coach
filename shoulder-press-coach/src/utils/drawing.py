"""Drawing helpers for overlays and pose UI."""

from __future__ import annotations
import cv2
import mediapipe as mp
from src.utils.geometry import Point

_MP_DRAWING = mp.solutions.drawing_utils

# BGR Colors
COLOR_GREEN = (0, 255, 0)
COLOR_RED = (0, 0, 255)
COLOR_WHITE = (255, 255, 255)

def draw_pose_landmarks(frame, pose_result, connections, is_correct: bool) -> None:
    """Draw MediaPipe pose landmarks on the frame. Color changes based on form."""
    if pose_result.raw_result.pose_landmarks:
        # Swap colors based on the state machine's assessment
        line_color = COLOR_GREEN if is_correct else COLOR_RED
        
        custom_style = _MP_DRAWING.DrawingSpec(color=line_color, thickness=3, circle_radius=2)
        landmark_style = _MP_DRAWING.DrawingSpec(color=COLOR_WHITE, thickness=2, circle_radius=2)

        _MP_DRAWING.draw_landmarks(
            frame,
            pose_result.raw_result.pose_landmarks,
            connections,
            landmark_style,
            custom_style,
        )

def draw_header(frame, rep_count: int, stage: str, breath: str, feedback_text: str, is_correct: bool) -> None:
    """Render the main coaching HUD."""
    # Expand the background box to fit 4 lines of text
    cv2.rectangle(frame, (10, 10), (450, 165), (30, 30, 30), -1)
    
    text_color = COLOR_GREEN if is_correct else COLOR_RED

    cv2.putText(frame, f"Reps: {rep_count} / 12", (25, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, COLOR_WHITE, 2)
    cv2.putText(frame, f"Stage: {stage}", (25, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 220, 255), 2)
    cv2.putText(frame, f"Breath: {breath}", (25, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 200, 0), 2)
    cv2.putText(frame, feedback_text, (25, 145), cv2.FONT_HERSHEY_SIMPLEX, 0.65, text_color, 2)

def draw_angle_label(frame, point: Point, angle: float, is_correct: bool) -> None:
    """Render the elbow angle near the elbow landmark."""
    label = f"{int(angle)} deg"
    text_color = COLOR_GREEN if is_correct else COLOR_RED
    text_position = (point.x + 15, point.y - 15)
    cv2.putText(frame, label, text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.6, text_color, 2)