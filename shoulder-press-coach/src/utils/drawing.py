"""Drawing helpers for overlays and pose UI."""

from __future__ import annotations
import cv2
import math
import mediapipe as mp
from src.utils.geometry import Point

_MP_DRAWING = mp.solutions.drawing_utils

# BGR Colors
COLOR_GREEN = (0, 255, 0)
COLOR_RED = (0, 0, 255)
COLOR_WHITE = (255, 255, 255)
COLOR_GOLD = (0, 215, 255)
COLOR_TEAL = (128, 128, 0)

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

def draw_header(frame, rep_count: int, rep_goal: int, stage: str, breath: str, feedback_text: str, is_correct: bool) -> None:
    """Render the main coaching HUD."""
    # Expand the background box to fit 4 lines of text
    cv2.rectangle(frame, (10, 10), (450, 165), (30, 30, 30), -1)
    
    text_color = COLOR_GREEN if is_correct else COLOR_RED

    cv2.putText(frame, f"Reps: {rep_count} / {rep_goal}", (25, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, COLOR_WHITE, 2)
    cv2.putText(frame, f"Stage: {stage}", (25, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 220, 255), 2)
    cv2.putText(frame, f"Breath: {breath}", (25, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 200, 0), 2)
    cv2.putText(frame, feedback_text, (25, 145), cv2.FONT_HERSHEY_SIMPLEX, 0.65, text_color, 2)

def draw_angle_label(frame, point: Point, angle: float, is_correct: bool) -> None:
    """Render the elbow angle near the elbow landmark."""
    label = f"{int(angle)} deg"
    text_color = COLOR_GREEN if is_correct else COLOR_RED
    text_position = (point.x + 15, point.y - 15)
    cv2.putText(frame, label, text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.6, text_color, 2)

def draw_correction_feedback(frame, metrics) -> None:
    """Draw visual cues to help the user correct their posture."""
    if metrics and metrics.is_flaring:
        # Start at the elbow
        start_point = (metrics.elbow_point.x, metrics.elbow_point.y)
        
        # Calculate a target point tucked in toward the body
        # (Moving the elbow horizontally toward the wrist's x-position)
        direction = -1 if metrics.elbow_point.x > metrics.wrist_point.x else 1
        
        # We'll draw an arrow roughly 40 pixels long pointing inward
        target_x = metrics.elbow_point.x + (direction * 40)
        end_point = (target_x, metrics.elbow_point.y)

        # Draw a thick Red Arrow pointing inward
        cv2.arrowedLine(frame, start_point, end_point, (0, 0, 255), 5, tipLength=0.3)
        
        # Add a text label above the arrow
        cv2.putText(frame, "TUCK IN", (start_point[0] - 40, start_point[1] - 20), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

def draw_completion_animation(frame, elapsed_time: float, rep_goal: int) -> None:
    """Render a short completion animation after the rep goal is reached."""
    duration = 2.0
    progress = min(max(elapsed_time / duration, 0.0), 1.0)
    height, width = frame.shape[:2]
    center = (width // 2, height // 2)

    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (width, height), (20, 20, 20), -1)
    cv2.addWeighted(overlay, 0.35, frame, 0.65, 0, frame)

    pulse = 0.5 + 0.5 * math.sin(progress * math.pi * 4)
    outer_radius = int(min(width, height) * (0.12 + 0.18 * progress))
    middle_radius = max(outer_radius - 26, 10)
    inner_radius = max(outer_radius - 52, 8)

    cv2.circle(frame, center, outer_radius, COLOR_GOLD, 6)
    cv2.circle(frame, center, middle_radius, COLOR_TEAL, 4)
    cv2.circle(frame, center, inner_radius, (255, 255, 255), -1)

    accent_y = int(height * (0.20 + 0.03 * pulse))
    cv2.circle(frame, (center[0] - 150, accent_y), 14, COLOR_GOLD, -1)
    cv2.circle(frame, (center[0] + 150, accent_y), 14, COLOR_TEAL, -1)
    cv2.circle(frame, (center[0] - 110, accent_y + 36), 10, COLOR_WHITE, -1)
    cv2.circle(frame, (center[0] + 110, accent_y + 36), 10, COLOR_WHITE, -1)

    cv2.putText(
        frame,
        f"{rep_goal} COMPLETE",
        (center[0] - 145, center[1] - 10),
        cv2.FONT_HERSHEY_DUPLEX,
        1.0 + (0.05 * pulse),
        (20, 20, 20),
        2,
    )
    cv2.putText(
        frame,
        "Nice press set",
        (center[0] - 95, center[1] + 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        COLOR_GOLD,
        2,
    )