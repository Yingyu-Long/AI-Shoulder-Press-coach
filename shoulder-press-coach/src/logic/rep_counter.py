"""Rep counting state machine and strict form coaching."""

from __future__ import annotations
from dataclasses import dataclass
from src.detector.exercise_detector import PressMetrics

@dataclass
class CoachingState:
    frontend_stage: str
    breath: str
    feedback: str
    is_correct: bool
    reps: int

class RepCounter:
    """Track reps using strict timing and angle tolerances."""

    def __init__(self):
        self.reps = 0
        self.backend_stage = "BOTTOM" 
        self.state_entry_time = 0.0
        
        # Timers for the isometric holds
        self.bottom_hold_start = None
        self.top_hold_start = None
        
        # Flag to unlock the press stage after the 2.0s hold
        self.ready_to_press = False 
        
        self.max_up_angle = 0.0
        self.min_down_angle = 360.0

    def update(self, metrics: PressMetrics, current_time: float) -> CoachingState:
        if not metrics.visibility_ok:
            return CoachingState("Unknown", "-", "Please step into the frame", False, self.reps)

        # 1. Check for workout completion
        if self.reps >= 12:
            return CoachingState("Relax", "Breathe", "Workout Complete! Great job.", True, self.reps)

        # 2. Set defaults for a "Good" frame
        is_correct = True
        feedback = "Green -> You are doing good!"
        frontend_stage = "-"  
        breath = "Breathe"

        # 3. Global Posture Check (Flaring)
        if metrics.is_flaring:
            is_correct = False
            feedback = "Don't Flare your Elbows Out"

        # 4. State Machine Logic
        if self.backend_stage == "BOTTOM":
            
            # A. Check if they are in the correct starting position
            if metrics.is_at_eye_level and not metrics.is_flaring:
                if self.bottom_hold_start is None:
                    self.bottom_hold_start = current_time
                    frontend_stage = "Hold" 
                elif current_time - self.bottom_hold_start >= 2.0: 
                    self.ready_to_press = True
                    feedback = "Good hold! Press up." 
                    frontend_stage = "Press"
                    breath = "Exhale"
                else:
                    frontend_stage = "Hold" # Keep showing Hold during the 2.0s wait
            else:
                # B. Not at eye level. 
                if self.ready_to_press:
                    feedback = "Good hold! Press up."
                    frontend_stage = "Press"
                    breath = "Exhale"
                else:
                    self.bottom_hold_start = None
                    if is_correct: 
                        is_correct = False
                        feedback = "Bring dumbbells to eye level"

            # C. Transition to UP stage once they cross the angle threshold
            if self.ready_to_press and metrics.elbow_angle > 105: 
                self.backend_stage = "UP"
                self.state_entry_time = current_time
                self.max_up_angle = metrics.elbow_angle
                
                # Reset bottom states for the next rep
                self.ready_to_press = False 
                self.bottom_hold_start = None

        elif self.backend_stage == "UP":
            frontend_stage, breath = "Press", "Exhale"
            self.max_up_angle = max(self.max_up_angle, metrics.elbow_angle)

            # Tolerance check: Angle should not decrease by more than 5 degrees
            if metrics.elbow_angle < (self.max_up_angle - 5):
                is_correct = False
                feedback = f"Keep your elbow tight, degree: {int(metrics.elbow_angle)}"
            
            # Timeout check: If pressing takes more than 3 seconds
            if (current_time - self.state_entry_time) > 3.0:
                is_correct = False
                feedback = "Fully extend your arms!"

            # Transition to TOP (Target adjusted to 140 degrees)
            if metrics.elbow_angle >= 140:
                self.backend_stage = "TOP"
                self.top_hold_start = current_time # Start the 1-second top timer

        elif self.backend_stage == "TOP":
            frontend_stage, breath = "Top", "Breathe"
            
            time_held = current_time - self.top_hold_start

            if time_held < 1.0:
                feedback = "Hold it at the top..."
                
                # If they drop their arms too early (gave a 5-degree buffer)
                if metrics.elbow_angle < 135:
                    is_correct = False
                    feedback = "Don't drop yet! Hold for 1 second."
            else:
                # 1 second has successfully passed. Transition directly to DOWN.
                self.backend_stage = "DOWN"
                self.state_entry_time = current_time
                self.min_down_angle = metrics.elbow_angle
                self.top_hold_start = None # Reset the top timer

        elif self.backend_stage == "DOWN":
            frontend_stage, breath = "Descent", "Inhale"
            self.min_down_angle = min(self.min_down_angle, metrics.elbow_angle)

            # Tolerance check: Angle should not increase by more than 5 degrees during descent
            if metrics.elbow_angle > (self.min_down_angle + 5):
                is_correct = False
                feedback = f"Keep your elbow tight, degree: {int(metrics.elbow_angle)}"

            # Transition to Rest/Bottom
            if metrics.is_at_eye_level:
                self.backend_stage = "BOTTOM"
                self.bottom_hold_start = None
                self.ready_to_press = False 
                self.reps += 1

        # Override feedback if global flaring was detected above
        if not is_correct and metrics.is_flaring:
            feedback = "Don't Flare your Elbows Out"

        return CoachingState(frontend_stage, breath, feedback, is_correct, self.reps)