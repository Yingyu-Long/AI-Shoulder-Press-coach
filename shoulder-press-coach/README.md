# shoulder-press-coach

Simple desktop webcam app that detects a shoulder press, counts reps, and shows live coaching feedback using OpenCV and MediaPipe Pose.

## Features

- Uses a local webcam for live video
- Detects pose landmarks with MediaPipe Pose
- Tracks a right-arm shoulder press with adjustable thresholds
- Counts reps using a small state machine
- Displays rep count, stage, elbow angle, and coaching text
- Keeps the code modular so it is easy to extend later

## Project Structure

```text
shoulder-press-coach/
  app.py
  requirements.txt
  README.md
  src/
    __init__.py
    detector/
      __init__.py
      pose_detector.py
      exercise_detector.py
    logic/
      __init__.py
      rep_counter.py
      feedback.py
    utils/
      __init__.py
      geometry.py
      drawing.py
```

## Setup

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

Press `q` or `Esc` to close the app.

## Notes

- The MVP uses the right arm only to keep the logic simple.
- Stage detection combines elbow angle and wrist-vs-shoulder height.
- Thresholds live in `src/detector/exercise_detector.py` and can be tuned quickly for your demo.
