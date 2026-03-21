"""MediaPipe pose wrapper for webcam frames."""

from __future__ import annotations

from dataclasses import dataclass

import cv2
import mediapipe as mp


@dataclass
class PoseResult:
    """Container for pose detection output."""

    landmarks: object | None
    raw_result: object


class PoseDetector:
    """Small wrapper around MediaPipe Pose setup and inference."""

    def __init__(
        self,
        min_detection_confidence: float = 0.5,
        min_tracking_confidence: float = 0.5,
    ) -> None:
        self._mp_pose = mp.solutions.pose
        self._pose = self._mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            enable_segmentation=False,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )
        self.pose_connections = self._mp_pose.POSE_CONNECTIONS

    def process(self, frame):
        """Run pose detection on a BGR frame."""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self._pose.process(rgb_frame)
        landmarks = result.pose_landmarks.landmark if result.pose_landmarks else None
        return PoseResult(landmarks=landmarks, raw_result=result)

    def close(self) -> None:
        """Release MediaPipe resources."""
        self._pose.close()
