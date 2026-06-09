import sqlite3
import re
from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__)

def get_db():
    conn = sqlite3.connect("database/users.db")
    conn.row_factory = sqlite3.Row
    return conn

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            return redirect(url_for("main.index"))

        return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Email validation
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_pattern, username):
            return render_template("register.html", error="Please enter a valid email address.")

        # Password requirements
        if len(password) < 8:
            return render_template("register.html", error="Password must be at least 8 characters long.")

        if not re.search(r"[A-Z]", password):
            return render_template("register.html", error="Password must contain at least one capital letter.")

        if not re.search(r"[0-9]", password):
            return render_template("register.html", error="Password must contain at least one number.")

        # Hash AFTER validation
        hashed_password = generate_password_hash(password)

        db = get_db()
        try:
            db.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            db.commit()
        except sqlite3.IntegrityError:
            return render_template("register.html", error="This email is already registered.")

        return redirect(url_for("auth.login"))

    return render_template("register.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))