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