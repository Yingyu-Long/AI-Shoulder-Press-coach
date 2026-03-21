"""Drawing helpers for overlays and pose UI."""

from __future__ import annotations

import cv2
import mediapipe as mp

from src.utils.geometry import Point


_MP_DRAWING = mp.solutions.drawing_utils
_LANDMARK_STYLE = _MP_DRAWING.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2)
_CONNECTION_STYLE = _MP_DRAWING.DrawingSpec(color=(66, 245, 164), thickness=2, circle_radius=2)


def draw_pose_landmarks(frame, pose_result, connections) -> None:
    """Draw MediaPipe pose landmarks on the frame."""
    if pose_result.raw_result.pose_landmarks:
        _MP_DRAWING.draw_landmarks(
            frame,
            pose_result.raw_result.pose_landmarks,
            connections,
            _LANDMARK_STYLE,
            _CONNECTION_STYLE,
        )


def draw_header(frame, rep_count: int, stage: str, feedback_text: str) -> None:
    """Render the main coaching HUD."""
    cv2.rectangle(frame, (10, 10), (360, 130), (30, 30, 30), -1)
    cv2.putText(frame, f"Reps: {rep_count}", (25, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
    cv2.putText(frame, f"Stage: {stage}", (25, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 220, 255), 2)
    cv2.putText(frame, feedback_text, (25, 115), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (80, 255, 120), 2)


def draw_angle_label(frame, point: Point, angle: float) -> None:
    """Render the elbow angle near the elbow landmark."""
    label = f"{int(angle)} deg"
    text_position = (point.x + 10, point.y - 10)
    cv2.putText(frame, label, text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
