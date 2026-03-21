"""Shoulder press-specific measurement logic."""

from __future__ import annotations
from dataclasses import dataclass
import mediapipe as mp

from src.utils.geometry import Point, angle_between_points, landmark_to_point

@dataclass
class PressMetrics:
    """Computed measurements used for stage detection and feedback."""
    elbow_angle: float
    visibility_ok: bool
    is_at_eye_level: bool
    is_flaring: bool
    shoulder_point: Point
    elbow_point: Point
    wrist_point: Point
    nose_point: Point


class ShoulderPressDetector:
    """Analyze a single arm for shoulder press movement."""

    def __init__(self, side: str = "right") -> None:
        if side.lower() != "right":
            raise ValueError("This MVP currently supports the right side only.")
        self.side = side.lower()
        self._pose_landmark = mp.solutions.pose.PoseLandmark

    def analyze(self, landmarks, frame_shape) -> PressMetrics:
        """Extract angles and relative positions for the active arm."""
        height, width = frame_shape[:2]

        shoulder = landmarks[self._pose_landmark.RIGHT_SHOULDER]
        elbow = landmarks[self._pose_landmark.RIGHT_ELBOW]
        wrist = landmarks[self._pose_landmark.RIGHT_WRIST]
        nose = landmarks[self._pose_landmark.NOSE] # Used for eye-level check

        shoulder_point = landmark_to_point(shoulder, width, height)
        elbow_point = landmark_to_point(elbow, width, height)
        wrist_point = landmark_to_point(wrist, width, height)
        nose_point = landmark_to_point(nose, width, height)

        elbow_angle = angle_between_points(shoulder_point, elbow_point, wrist_point)
        visibility_ok = min(shoulder.visibility, elbow.visibility, wrist.visibility, nose.visibility) > 0.5

        # Eye level heuristic: Wrist is roughly at the same height as the nose/eyes
        is_at_eye_level = abs(wrist_point.y - nose_point.y) < (height * 0.15)
        
        # Flaring heuristic: The wrist and elbow should be vertically aligned. 
        # If the horizontal distance is too large, the elbow is flaring out.
        is_flaring = abs(wrist_point.x - elbow_point.x) > (width * 0.12)

        return PressMetrics(
            elbow_angle=elbow_angle,
            visibility_ok=visibility_ok,
            is_at_eye_level=is_at_eye_level,
            is_flaring=is_flaring,
            shoulder_point=shoulder_point,
            elbow_point=elbow_point,
            wrist_point=wrist_point,
            nose_point=nose_point,
        )