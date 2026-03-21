"""Rep counting state machine for shoulder presses."""

from __future__ import annotations

from dataclasses import dataclass

from src.detector.exercise_detector import PressMetrics


@dataclass
class RepCounter:
    """Track reps using a DOWN -> UP -> DOWN movement cycle."""

    reps: int = 0
    stage: str = "DOWN"
    _seen_up: bool = False

    def update(self, metrics: PressMetrics) -> tuple[str, int, str | None]:
        """Update stage and rep count from the latest measurements."""
        if not metrics.visibility_ok:
            return self.stage, self.reps, None

        rep_event = None

        if metrics.inferred_stage == "DOWN":
            if self.stage == "UP" and self._seen_up:
                self.reps += 1
                rep_event = "good_rep"
            self.stage = "DOWN"

        elif metrics.inferred_stage == "UP":
            self.stage = "UP"
            self._seen_up = True

        return self.stage, self.reps, rep_event
