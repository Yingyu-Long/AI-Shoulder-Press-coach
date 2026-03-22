# shoulder-press-coach

Simple desktop webcam app that detects a shoulder press, counts reps, and shows live coaching feedback using OpenCV and MediaPipe Pose.

## Features

- Uses a local webcam for live video
- Detects pose landmarks with MediaPipe Pose
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

1. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

Press `q` or `Esc` to close the app.
