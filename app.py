from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

# -------------------------------
# Step 1: Initialize Flask App
# -------------------------------
app = Flask(__name__)

# -------------------------------
# Step 2: Configure Database (absolute path)
# -------------------------------
basedir = os.path.abspath(os.path.dirname(__file__))  # Current folder of app.py
db_path = os.path.join(basedir, "tasks.db")          # Full path to tasks.db
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# -------------------------------
# Step 3: Define Task Model
# -------------------------------
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default="pending")  # pending/done

# -------------------------------
# Step 4: Routes
# -------------------------------

# Home route
@app.route("/")
def home():
    return "Hello World! Welcome to Task Manager."

# GET /tasks -> Fetch all tasks
@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    output = [{"id": t.id, "title": t.title, "status": t.status} for t in tasks]
    return jsonify(output), 200

# POST /tasks -> Create a new task
@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json()
    task_title = data.get("title")

    if task_title:
        new_task = Task(title=task_title)
        db.session.add(new_task)
        db.session.commit()
        return jsonify({
            "message": "Task added",
            "task": {"id": new_task.id, "title": new_task.title, "status": new_task.status}
        }), 201

    return jsonify({"error": "Task title is required"}), 400

# -------------------------------
# Step 5: Run App & Create DB
# -------------------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Creates tasks table in tasks.db inside TaskManager folder
    app.run(debug=True)
