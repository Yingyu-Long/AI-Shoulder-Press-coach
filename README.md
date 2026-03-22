# 🏋️‍♂️ AI Personal Trainer (Exercise Coach)

An intelligent, real-time webcam exercise coach powered by Computer Vision. This application acts as your personal virtual trainer—counting your reps, analyzing your form, and providing visual corrections on the fly to ensure you get a safe and effective workout.

Currently, the trainer specializes in the **Shoulder Press**, featuring a modular architecture designed to support many more exercises in the future.

---

## ✨ Features

* **Real-Time Rep Tracking:** Automatically counts reps using a strict state-machine that tracks the bottom, pressing, top, and descending phases of your movement.
* **Strict Form Coaching:** It doesn't just count; it judges. The app enforces:
  * Proper starting depth (dumbbells at eye level).
  * Full arm extension at the top.
  * Isometric holds (pausing at the top and bottom of the movement).
  * Hand convergence (bringing hands closer together during the press).
* **Visual Posture Correction:** If you break form (e.g., flaring your elbows out too far), the app draws corrective visual cues—like a red "TUCK IN" arrow—directly on your joints to show you exactly how to fix it.
* **Dynamic HUD & Breathing Cues:** On-screen prompts guide your breathing (Inhale on the way down, Exhale on the push) and display your current stage in real-time.
* **Custom Workout Goals:** Set your target reps before you start. Hitting your goal triggers a custom celebration animation!
* **Quick Reset:** Press `R` at any time to reset your current set without restarting the app.

---

## 🛠️ Installation & Setup

### Prerequisites
* Python 3.8+
* A working webcam

### 1. Clone the repository
```bash
git clone [https://github.com/YourUsername/AI_Exercise-Coach.git](https://github.com/YourUsername/AI_Exercise-Coach.git)
cd AI_Exercise-Coach