from flask import Flask, jsonify, request

app = Flask(__name__)

tasks= []

@app.route('/')
def home():
    return "Hello Mustafa"

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json()
    task_name = data.get("name")
    if task_name:
        tasks.append({"name": task_name})  # ✅ FIXED
        return jsonify({"message": "Task added", "tasks": tasks}), 201
    return jsonify({"error": "Task name is required"}), 400


if __name__ == "__main__":
    app.run(debug=True)

