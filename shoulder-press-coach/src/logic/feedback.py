"""Generate simple coaching messages from pose measurements."""

from __future__ import annotations

from src.detector.exercise_detector import PressMetrics


def generate_feedback(metrics: PressMetrics | None, stage: str, rep_event: str | None) -> str:
    """Return a short coaching cue for the current frame."""
    if metrics is None:
        return "Get in frame"

    if not metrics.visibility_ok:
        return "Bring your right arm into view"

    if rep_event == "good_rep":
        return "Good rep"

    if stage == "DOWN":
        if metrics.elbow_angle < 70:
            return "Bottom position: lower with control"
        if metrics.wrist_y_delta <= 0:
            return "Setup: bring your wrist below shoulder level"
        return "Bottom position: press up"

    if stage == "UP":
        if metrics.elbow_angle < 165 and not metrics.wrist_above_shoulder:
            return "Top position: press higher and straighten your elbow"
        if metrics.elbow_angle < 165:
            return "Top position: straighten your elbow more"
        if not metrics.wrist_above_shoulder:
            return "Top position: press your wrist higher overhead"
        return "Top position: lower with control"

    if metrics.elbow_angle < 120:
        if metrics.wrist_y_delta > 0:
            return "Mid press: drive upward"
        return "Transition: keep pressing overhead"

    return "Transition: stay steady"
