from flask import Blueprint, render_template, session, redirect, url_for

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    return render_template("index.html")

@main_bp.route("/dashboard")
def dashboard():
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))
    return render_template("dashboard.html")

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

from flask import Blueprint, render_template, session, redirect, url_for, request

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    return render_template("index.html")

@main_bp.route("/dashboard")
def dashboard():
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))
    return render_template("dashboard.html")

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

# SAVE WORKOUT ROUTE
@main_bp.route("/workout/save", methods=["POST"])
def save_workout():
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))

    user_id = session["user_id"]
    template_name = request.form.get("template_name")

#js print data to see if it works
    print("Saving workout for user:", user_id)
    print("Template:", template_name)
    print("Form data:", request.form)

    # Redirect back to dashboard after saving
    return redirect(url_for("main.dashboard"))

    user_id = session["user_id"]
    template_name = request.form.get("template_name")

    import sqlite3
    conn = sqlite3.connect("database/users.db")
    cursor = conn.cursor()

    # 1. Create workout log entry
    cursor.execute("""
        INSERT INTO workout_logs (user_id, template_name, date)
        VALUES (?, ?, datetime('now'))
    """, (user_id, template_name))

    workout_id = cursor.lastrowid

    # 2. Loop through all set inputs
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