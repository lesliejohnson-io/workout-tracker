"""
Workout Tracker Flask Application
A mobile-friendly web app to view workouts and track progress.
"""

import os
import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for
from workouts import WORKOUTS, get_workout

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-prod")

# Simple file-based storage for progress (works on Render free tier)
PROGRESS_FILE = "/tmp/workout_progress.json"


def load_progress():
    """Load progress data from file."""
    try:
        if os.path.exists(PROGRESS_FILE):
            with open(PROGRESS_FILE, "r") as f:
                return json.load(f)
    except (json.JSONDecodeError, IOError):
        pass
    return {}


def save_progress(progress):
    """Save progress data to file."""
    try:
        with open(PROGRESS_FILE, "w") as f:
            json.dump(progress, f)
    except IOError:
        pass


@app.route("/")
def home():
    """Home page showing all workouts."""
    return render_template("home.html", workouts=WORKOUTS)


@app.route("/workout/<workout_id>")
def workout_detail(workout_id):
    """Display a specific workout with progress tracking."""
    workout = get_workout(workout_id)
    if not workout:
        return redirect(url_for("home"))

    progress = load_progress()
    today = datetime.now().strftime("%Y-%m-%d")
    workout_key = f"{today}_{workout_id.upper()}"
    workout_progress = progress.get(workout_key, {})

    return render_template(
        "workout.html",
        workout_id=workout_id.upper(),
        workout=workout,
        progress=workout_progress,
        today=today
    )


@app.route("/api/progress", methods=["POST"])
def update_progress():
    """API endpoint to update exercise progress."""
    data = request.json
    workout_id = data.get("workout_id")
    exercise_index = data.get("exercise_index")
    set_number = data.get("set_number")
    completed = data.get("completed", False)
    reps = data.get("reps")
    weight = data.get("weight")

    progress = load_progress()
    today = datetime.now().strftime("%Y-%m-%d")
    workout_key = f"{today}_{workout_id}"

    if workout_key not in progress:
        progress[workout_key] = {}

    exercise_key = f"exercise_{exercise_index}"
    if exercise_key not in progress[workout_key]:
        progress[workout_key][exercise_key] = {}

    set_key = f"set_{set_number}"
    progress[workout_key][exercise_key][set_key] = {
        "completed": completed,
        "reps": reps,
        "weight": weight,
        "timestamp": datetime.now().isoformat()
    }

    save_progress(progress)
    return jsonify({"success": True})


@app.route("/api/progress/<workout_id>", methods=["GET"])
def get_progress(workout_id):
    """Get progress for a specific workout today."""
    progress = load_progress()
    today = datetime.now().strftime("%Y-%m-%d")
    workout_key = f"{today}_{workout_id.upper()}"
    return jsonify(progress.get(workout_key, {}))


@app.route("/history")
def history():
    """View workout history."""
    progress = load_progress()
    # Sort by date, most recent first
    sorted_keys = sorted(progress.keys(), reverse=True)
    history_data = []

    for key in sorted_keys[:30]:  # Last 30 entries
        parts = key.split("_")
        if len(parts) == 2:
            date, workout_id = parts
            workout = get_workout(workout_id)
            if workout:
                completed_sets = sum(
                    1 for ex in progress[key].values()
                    for s in ex.values()
                    if isinstance(s, dict) and s.get("completed")
                )
                total_sets = len(workout["exercises"]) * 2
                history_data.append({
                    "date": date,
                    "workout_id": workout_id,
                    "workout_name": workout["name"],
                    "completed_sets": completed_sets,
                    "total_sets": total_sets
                })

    return render_template("history.html", history=history_data)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
