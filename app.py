from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
from flask import request, redirect, render_template

# -----------------------
# App setup
# -----------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = 'learning-secret-key'  # needed for session

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir,'tasks.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# -----------------------
# Database Models
# -----------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    father_name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)

    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default="pending")

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# -----------------------
# Helper: login check
# -----------------------
def login_required():
    return "user_id" in session

# -----------------------
# ROUTES
# -----------------------

# HOME (just info)

@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")


@app.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")


@app.route("/register", methods=["GET"])
def register_page():
    return render_template("register.html")


@app.route("/dashboard", methods=["GET"])
def dashboard_page():
    if "user_id" not in session:
        return redirect("/login")
    return render_template("dashboard.html")


# -----------------------
# REGISTER
# -----------------------
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()  # expects JSON from JS
    if not data:
        return jsonify({"error": "No data received"}), 400

    first_name = data.get("first_name")
    last_name = data.get("last_name")
    father_name = data.get("father_name")
    age = data.get("age")
    username = data.get("username")
    password = data.get("password")
    confirm_password = data.get("confirm_password")

    # validate
    if not all([first_name, last_name, father_name, age, username, password, confirm_password]):
        return jsonify({"error": "All fields are required"}), 400
    if password != confirm_password:
        return jsonify({"error": "Passwords do not match"}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 400

    hashed_password = generate_password_hash(password)

    user = User(
        first_name=first_name,
        last_name=last_name,
        father_name=father_name,
        age=age,
        username=username,
        password_hash=hashed_password
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


# -----------------------
# LOGIN
# -----------------------
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid credentials"}), 401

    session["user_id"] = user.id
    return jsonify({"message": "Login successful"}), 200


# -----------------------
# LOGOUT
# -----------------------
@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logged out"}), 200


# -----------------------
# TASKS
# -----------------------
@app.route("/tasks", methods=["GET"])
def get_tasks():
    if not login_required():
        return jsonify({"error": "Login required"}), 401

    tasks = Task.query.filter_by(user_id=session["user_id"]).all()

    return jsonify([
        {"id": t.id, "title": t.title, "status": t.status}
        for t in tasks
    ])


@app.route("/tasks", methods=["POST"])
def add_task():
    if not login_required():
        return jsonify({"error": "Login required"}), 401

    data = request.get_json()
    title = data.get("title")

    if not title:
        return jsonify({"error": "Title required"}), 400

    task = Task(title=title, user_id=session["user_id"])
    db.session.add(task)
    db.session.commit()

    return jsonify({"message": "Task added"}), 201


@app.route("/tasks/<int:id>", methods=["PUT"])
def update_task(id):
    if not login_required():
        return jsonify({"error": "Login required"}), 401

    task = Task.query.filter_by(id=id, user_id=session["user_id"]).first()
    if not task:
        return jsonify({"error": "Task not found"}), 404

    data = request.get_json()
    task.title = data.get("title", task.title)
    task.status = data.get("status", task.status)

    db.session.commit()
    return jsonify({"message": "Task updated"})


@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    if not login_required():
        return jsonify({"error": "Login required"}), 401

    task = Task.query.filter_by(id=id, user_id=session["user_id"]).first()
    if not task:
        return jsonify({"error": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted"})


# -----------------------
# RUN
# -----------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
