# Shoulder Press Coach

Desktop webcam app for tracking a right-arm shoulder press with live feedback, rep counting, and a simple completion animation.

## What It Does

- Uses your webcam for live pose tracking
- Detects the right shoulder, elbow, wrist, nose, and hand landmarks with MediaPipe Pose
- Counts reps with a stage-based state machine
- Shows live coaching feedback on screen
- Prompts for today's rep goal before the session starts
- Plays a short completion animation when the goal is reached
- Lets the user reset the workout by pressing `R`

## Current Coaching Rules

- `Elbow is too tight` if elbow angle is below `40`
- `Don't Flare your Elbows Out` during the press stage if elbow angle goes above `140`
- `Bring dumbbells to eye level` if the start position is not reached
- `Hold it at the top...` and `Don't drop yet! Hold for 1 second.` for the top hold
- `Fully extend your arms!` if the press takes too long

## Project Structure

```text
shoulder-press-coach/
  app.py
  requirements.txt
  README.md
  src/
    config.py
    detector/
      pose_detector.py
      exercise_detector.py
    logic/
      rep_counter.py
    utils/
      drawing.py
      geometry.py
```

## Requirements

- Python 3.10+
- Webcam access

Dependencies:

- `mediapipe==0.10.14`
- `opencv-python==4.10.0.84`
- `numpy==1.26.4`

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

When the app starts, it asks:

```text
How much do you wanna press today? [12]:
```

Press:

- `R` to reset the rep counter
- `Q` or `Esc` to quit

## How It Works

1. `app.py` starts the webcam loop and prompts for today's rep goal.
2. `src/detector/pose_detector.py` runs MediaPipe Pose on each frame.
3. `src/detector/exercise_detector.py` converts landmarks into shoulder-press metrics such as elbow angle and whether the hand is back at eye level.
4. `src/logic/rep_counter.py` manages the workout state machine: `BOTTOM -> UP -> TOP -> DOWN`.
5. `src/utils/drawing.py` renders the HUD, elbow-angle label, pose landmarks, and completion animation.

## Notes

- The app currently supports the right arm only.
- The rep goal is chosen at runtime, but the default goal lives in `src/config.py`.
- Thresholds are intentionally simple and can be tuned in `src/logic/rep_counter.py` and `src/detector/exercise_detector.py`.
