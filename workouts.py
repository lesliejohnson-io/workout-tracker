"""
Workout Routines Configuration
Contains predefined workout routines with exercises, sets, reps, and RPE targets.
"""

WORKOUTS = {
    "A": {
        "name": "Push Dominant",
        "duration": "30-35 minutes",
        "exercises": [
            {"name": "Barbell Back Squat", "sets": 2, "reps": "5-6", "rpe": "9"},
            {"name": "Incline Barbell Bench Press", "sets": 2, "reps": "6-8", "rpe": "9"},
            {"name": "Romanian Deadlift", "sets": 2, "reps": "6-8", "rpe": "8-9"},
            {"name": "Overhead Press", "sets": 2, "reps": "6-8", "rpe": "9"},
            {"name": "Dumbbell Bulgarian Split Squat", "sets": 2, "reps": "8-10 per leg", "rpe": "8"},
            {"name": "Weighted Dips", "sets": 2, "reps": "8-12", "rpe": "9"},
            {"name": "Cable Tricep Pushdowns", "sets": 2, "reps": "10-12", "rpe": "9"},
            {"name": "Standing Calf Raises", "sets": 2, "reps": "12-15", "rpe": "9"},
            {"name": "Plank Hold", "sets": 2, "reps": "45-60 seconds", "rpe": None},
        ]
    },
    "B": {
        "name": "Pull Dominant",
        "duration": "30-35 minutes",
        "exercises": [
            {"name": "Conventional Deadlift", "sets": 2, "reps": "5", "rpe": "9"},
            {"name": "Weighted Pull-ups", "sets": 2, "reps": "6-8", "rpe": "9"},
            {"name": "Front Squat", "sets": 2, "reps": "6-8", "rpe": "8-9"},
            {"name": "Barbell Bent-Over Row", "sets": 2, "reps": "6-8", "rpe": "9"},
            {"name": "Walking Lunges", "sets": 2, "reps": "10 per leg", "rpe": "8"},
            {"name": "Chest-Supported Dumbbell Row", "sets": 2, "reps": "8-10", "rpe": "9"},
            {"name": "Barbell Bicep Curl", "sets": 2, "reps": "8-10", "rpe": "9"},
            {"name": "Face Pulls", "sets": 2, "reps": "15-20", "rpe": "8"},
            {"name": "Hanging Leg Raises", "sets": 2, "reps": "10-15", "rpe": None},
        ]
    },
    "C": {
        "name": "Leg & Power Focus",
        "duration": "35-40 minutes",
        "exercises": [
            {"name": "Trap Bar Deadlift", "sets": 2, "reps": "5-6", "rpe": "9"},
            {"name": "Barbell Hip Thrust", "sets": 2, "reps": "8-10", "rpe": "9"},
            {"name": "Flat Barbell Bench Press", "sets": 2, "reps": "6-8", "rpe": "9"},
            {"name": "Goblet Squat", "sets": 2, "reps": "10-12", "rpe": "8-9"},
            {"name": "Pendlay Row", "sets": 2, "reps": "6-8", "rpe": "9"},
            {"name": "Leg Press", "sets": 2, "reps": "10-12", "rpe": "9"},
            {"name": "Hammer Curls", "sets": 2, "reps": "10-12", "rpe": "8"},
            {"name": "Lateral Raises", "sets": 2, "reps": "12-15", "rpe": "8-9"},
            {"name": "Ab Wheel Rollouts", "sets": 2, "reps": "8-12", "rpe": None},
        ]
    }
}


def get_workout(workout_id):
    """Get a specific workout by ID (A, B, or C)."""
    return WORKOUTS.get(workout_id.upper())


def list_workouts():
    """List all available workouts with their names."""
    return {k: v["name"] for k, v in WORKOUTS.items()}


def print_workout(workout_id):
    """Print a formatted workout routine."""
    workout = get_workout(workout_id)
    if not workout:
        print(f"Workout '{workout_id}' not found.")
        return

    print(f"\nWorkout {workout_id.upper()} - {workout['name']}")
    print(f"Duration: {workout['duration']}")
    print("-" * 60)

    for i, exercise in enumerate(workout["exercises"], 1):
        rpe_str = f"(RPE {exercise['rpe']})" if exercise["rpe"] else ""
        print(f"{i}. {exercise['name']} - {exercise['sets']} sets x {exercise['reps']} {rpe_str}")

    print()


if __name__ == "__main__":
    # Display all workouts when run directly
    for workout_id in WORKOUTS:
        print_workout(workout_id)
