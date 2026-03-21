"""Geometry helpers for pose calculations."""

from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass(frozen=True)
class Point:
    """Simple 2D point in image coordinates."""

    x: int
    y: int


def landmark_to_point(landmark, frame_width: int, frame_height: int) -> Point:
    """Convert a normalized MediaPipe landmark to image pixels."""
    return Point(
        x=int(landmark.x * frame_width),
        y=int(landmark.y * frame_height),
    )


def angle_between_points(a: Point, b: Point, c: Point) -> float:
    """Return the angle at point b formed by a-b-c."""
    radians = math.atan2(c.y - b.y, c.x - b.x) - math.atan2(a.y - b.y, a.x - b.x)
    angle = abs(math.degrees(radians))
    if angle > 180:
        angle = 360 - angle
    return angle
