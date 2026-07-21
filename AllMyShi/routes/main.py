from flask import Blueprint, render_template, session, redirect, url_for, request
import sqlite3
import calendar
from datetime import datetime
from exercise_library import exercise_library

main_bp = Blueprint("main", __name__)

# -------------------------
# BASIC ROUTES
# -------------------------

@main_bp.route("/")
def index():
    return render_template("index.html")

@main_bp.route("/dashboard")
def dashboard():
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))

    user_id = session["user_id"]

    conn = sqlite3.connect("database/users.db")
    cursor = conn.cursor()

    # Fetch all workouts
    cursor.execute("""
        SELECT id, template_name, date
        FROM workout_logs
        WHERE user_id = ?
        ORDER BY date DESC
    """, (user_id,))
    workouts = cursor.fetchall()

    history_data = []

    # Fetch sets for each workout
    for workout_id, template_name, date in workouts:
        cursor.execute("""
            SELECT exercise_name, set_number, reps, weight
            FROM workout_sets
            WHERE workout_id = ?
            ORDER BY exercise_name, set_number
        """, (workout_id,))
        sets = cursor.fetchall()

        history_data.append({
            "id": workout_id,
            "template": template_name,
            "date": date,
            "sets": sets
        })

    conn.close()

    return render_template("dashboard.html", history=history_data)

@main_bp.route("/workout")
def workout():
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))
    return render_template("workout.html")

@main_bp.route("/workout/push")
def push_workout():
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))
    return render_template("push.html")

@main_bp.route("/workout/pull")
def pull_workout():
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))
    return render_template("pull.html")

@main_bp.route("/workout/legs")
def legs_workout():
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))
    return render_template("legs.html")

@main_bp.route("/workout/upper")
def upper_workout():
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))
    return render_template("upper.html")

@main_bp.route("/workout/lower")
def lower_workout():
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))
    return render_template("lower.html")

@main_bp.route("/exercise-library")
def exercise_library_page():
    return render_template("exercise_library.html", exercises=exercise_library)

# -------------------------
# CUSTOM WORKOUT ROUTE
# -------------------------

@main_bp.route("/workout/custom")
def custom_workout():
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))

    conn = sqlite3.connect("database/users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM exercise_library ORDER BY name ASC")
    exercises = [row[0] for row in cursor.fetchall()]

    conn.close()

    return render_template("custom.html", exercises=exercises)

# -------------------------
# FIXED CALENDAR ROUTE
# -------------------------

@main_bp.route("/calendar")
def calendar_page():
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))

    user_id = session["user_id"]

    year = request.args.get("year", type=int)
    month = request.args.get("month", type=int)

    now = datetime.now()
    if not year:
        year = now.year
    if not month:
        month = now.month

    conn = sqlite3.connect("database/users.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT date FROM workout_logs
        WHERE user_id = ?
    """, (user_id,))
    rows = cursor.fetchall()
    conn.close()

    workout_dates = {row[0] for row in rows}

    cal = calendar.monthcalendar(year, month)

    prev_month = month - 1
    prev_year = year
    next_month = month + 1
    next_year = year

    if prev_month == 0:
        prev_month = 12
        prev_year -= 1

    if next_month == 13:
        next_month = 1
        next_year += 1

    return render_template(
        "calendar.html",
        cal=cal,
        year=year,
        month=month,
        workout_dates=workout_dates,
        prev_year=prev_year,
        prev_month=prev_month,
        next_year=next_year,
        next_month=next_month
    )

# -------------------------
# HISTORY ROUTE (still available if needed)
# -------------------------

@main_bp.route("/history")
def history():
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))

    user_id = session["user_id"]

    conn = sqlite3.connect("database/users.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, template_name, date
        FROM workout_logs
        WHERE user_id = ?
        ORDER BY date DESC
    """, (user_id,))
    workouts = cursor.fetchall()

    history_data = []

    for workout_id, template_name, date in workouts:
        cursor.execute("""
            SELECT exercise_name, set_number, reps, weight
            FROM workout_sets
            WHERE workout_id = ?
            ORDER BY exercise_name, set_number
        """, (workout_id,))
        sets = cursor.fetchall()

        history_data.append({
            "id": workout_id,
            "template": template_name,
            "date": date,
            "sets": sets
        })

    conn.close()

    return render_template("history.html", history=history_data)

# -------------------------
# SAVE WORKOUT ROUTE
# -------------------------

@main_bp.route("/workout/save", methods=["POST"])
def save_workout():
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))

    user_id = session["user_id"]
    template_name = request.form.get("template_name")

    conn = sqlite3.connect("database/users.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO workout_logs (user_id, template_name, date)
        VALUES (?, ?, date('now'))
    """, (user_id, template_name))

    workout_id = cursor.lastrowid

    for key in request.form:
        if key.startswith("reps_"):
            _, set_number, exercise = key.split("_")
            reps = request.form[key]
            weight = request.form.get(f"weight_{set_number}_{exercise}", 0)

            cursor.execute("""
                INSERT INTO workout_sets (workout_id, exercise_name, set_number, reps, weight, completed)
                VALUES (?, ?, ?, ?, ?, 1)
            """, (workout_id, exercise, set_number, reps, weight))

    conn.commit()
    conn.close()

    return redirect(url_for("main.dashboard"))

@main_bp.route("/exercise-library")
def exercise_library():
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))

    conn = sqlite3.connect("database/users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, gif_path FROM exercise_library ORDER BY name ASC")
    exercises = cursor.fetchall()

    conn.close()

    return render_template("exercise_library.html", exercises=exercises)
