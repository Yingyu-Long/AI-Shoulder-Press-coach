"""Shoulder press-specific measurement logic."""

from __future__ import annotations

from dataclasses import dataclass

import mediapipe as mp

from src.utils.geometry import Point, angle_between_points, landmark_to_point


@dataclass
class PressMetrics:
    """Computed measurements used for stage detection and feedback."""

    elbow_angle: float
    wrist_above_shoulder: bool
    wrist_y_delta: float
    elbow_y_delta: float
    visibility_ok: bool
    inferred_stage: str
    shoulder_point: Point
    elbow_point: Point
    wrist_point: Point


class ShoulderPressDetector:
    """Analyze a single arm for shoulder press movement."""

    def __init__(
        self,
        side: str = "right",
        down_angle_threshold: float = 105.0,
        up_angle_threshold: float = 155.0,
        overhead_margin_px: float = 15.0,
    ) -> None:
        if side.lower() != "right":
            raise ValueError("This MVP currently supports the right side only.")

        self.side = side.lower()
        self.down_angle_threshold = down_angle_threshold
        self.up_angle_threshold = up_angle_threshold
        self.overhead_margin_px = overhead_margin_px
        self._pose_landmark = mp.solutions.pose.PoseLandmark

    def analyze(self, landmarks, frame_shape) -> PressMetrics:
        """Extract angles and relative positions for the active arm."""
        height, width = frame_shape[:2]

        shoulder = landmarks[self._pose_landmark.RIGHT_SHOULDER]
        elbow = landmarks[self._pose_landmark.RIGHT_ELBOW]
        wrist = landmarks[self._pose_landmark.RIGHT_WRIST]

        shoulder_point = landmark_to_point(shoulder, width, height)
        elbow_point = landmark_to_point(elbow, width, height)
        wrist_point = landmark_to_point(wrist, width, height)

        elbow_angle = angle_between_points(shoulder_point, elbow_point, wrist_point)
        wrist_y_delta = wrist_point.y - shoulder_point.y
        elbow_y_delta = elbow_point.y - shoulder_point.y
        wrist_above_shoulder = wrist_point.y < (shoulder_point.y - self.overhead_margin_px)
        visibility_ok = min(shoulder.visibility, elbow.visibility, wrist.visibility) > 0.5

        inferred_stage = self._infer_stage(elbow_angle, wrist_above_shoulder, wrist_y_delta)

        return PressMetrics(
            elbow_angle=elbow_angle,
            wrist_above_shoulder=wrist_above_shoulder,
            wrist_y_delta=wrist_y_delta,
            elbow_y_delta=elbow_y_delta,
            visibility_ok=visibility_ok,
            inferred_stage=inferred_stage,
            shoulder_point=shoulder_point,
            elbow_point=elbow_point,
            wrist_point=wrist_point,
        )

    def _infer_stage(
        self,
        elbow_angle: float,
        wrist_above_shoulder: bool,
        wrist_y_delta: float,
    ) -> str:
        """Map current measurements to a coarse movement stage."""
        if elbow_angle >= self.up_angle_threshold and wrist_above_shoulder:
            return "UP"

        if elbow_angle <= self.down_angle_threshold and wrist_y_delta > 0:
            return "DOWN"

        return "MID"
