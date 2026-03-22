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
    flare_error_px: int = 0


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
        nose = landmarks[self._pose_landmark.NOSE]
        
        # New: Grab the 3 points of the hand to track the dumbbell handle
        pinky = landmarks[self._pose_landmark.RIGHT_PINKY]
        index = landmarks[self._pose_landmark.RIGHT_INDEX]
        thumb = landmarks[self._pose_landmark.RIGHT_THUMB]

        shoulder_point = landmark_to_point(shoulder, width, height)
        elbow_point = landmark_to_point(elbow, width, height)
        wrist_point = landmark_to_point(wrist, width, height)
        nose_point = landmark_to_point(nose, width, height)
        
        pinky_point = landmark_to_point(pinky, width, height)
        index_point = landmark_to_point(index, width, height)
        thumb_point = landmark_to_point(thumb, width, height)

        elbow_angle = angle_between_points(shoulder_point, elbow_point, wrist_point)
        
        # Ensure the hand is also visible
        visibility_ok = min(
            shoulder.visibility, elbow.visibility, wrist.visibility, 
            nose.visibility, pinky.visibility, index.visibility, thumb.visibility
        ) > 0.5

        # Calculate the center of the grip by averaging the 3 hand points
        hand_center_y = (pinky_point.y + index_point.y + thumb_point.y) / 3.0
        
        # Find the highest point of the hand (minimum y value in image coordinates)
        # This guarantees no part of your hand triggers it while still above your head
        highest_hand_y = min(pinky_point.y, index_point.y, thumb_point.y)

        # Eye level heuristic: The hand center must be near the nose, AND 
        # the top of the hand must be pushed down into the zone.
        # Tightened the margin to 10% of frame height to prevent early triggers.
        is_at_eye_level = (
            abs(hand_center_y - nose_point.y) < (height * 0.10) and 
            highest_hand_y > (nose_point.y - height * 0.12)
        )
        
        # Refined Flaring Logic: 
        # In a good press, the elbow should stay roughly under the wrist.
        # Calculate the horizontal distance between wrist and elbow
        horizontal_gap = abs(wrist_point.x - elbow_point.x)
        flare_threshold = width * 0.12
    
        is_flaring = horizontal_gap > flare_threshold
        flare_error_px = int(horizontal_gap - flare_threshold) if is_flaring else 0

        return PressMetrics(
            elbow_angle=elbow_angle,
            visibility_ok=visibility_ok,
            is_at_eye_level=is_at_eye_level,
            is_flaring=is_flaring,
            flare_error_px=flare_error_px,
            shoulder_point=shoulder_point,
            elbow_point=elbow_point,
            wrist_point=wrist_point,
            nose_point=nose_point,
        )