from flask import Flask, jsonify, request

app = Flask(__name__)


# A dictionary is our temporary in-memory data store. Restarting the server resets it.
tasks = {
    1: {
        "id": 1,
        "title": "Learn Flask",
        "description": "Build a simple REST API",
        "completed": False,
    },
    2: {
        "id": 2,
        "title": "Try the API",
        "description": "Send a request with curl",
        "completed": False,
    },
}
next_task_id = 3


@app.route("/", methods=["GET"])
def welcome():
    return jsonify({"message": "Welcome to the Task API"})


@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(list(tasks.values()))


@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = tasks.get(task_id)
    if task is None:
        return jsonify({"error": "Task not found"}), 404

    return jsonify(task)


@app.route("/tasks", methods=["POST"])
def create_task():
    global next_task_id

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be valid JSON"}), 400

    title = data.get("title")
    if not isinstance(title, str) or not title.strip():
        return jsonify({"error": "'title' is required"}), 400

    task = {
        "id": next_task_id,
        "title": title,
        "description": data.get("description", ""),
        "completed": data.get("completed", False),
    }
    tasks[next_task_id] = task
    next_task_id += 1

    return jsonify(task), 201


@app.route("/tasks/<int:task_id>", methods=["PATCH"])
def update_task(task_id):
    task = tasks.get(task_id)
    if task is None:
        return jsonify({"error": "Task not found"}), 404

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be valid JSON"}), 400

    if "title" in data:
        if not isinstance(data["title"], str) or not data["title"].strip():
            return jsonify({"error": "'title' must be a non-empty string"}), 400
        task["title"] = data["title"]

    # PATCH changes only fields supplied by the client.
    for field in ("description", "completed"):
        if field in data:
            task[field] = data[field]

    return jsonify(task)


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    if task_id not in tasks:
        return jsonify({"error": "Task not found"}), 404

    del tasks[task_id]
    return "", 204


def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()
