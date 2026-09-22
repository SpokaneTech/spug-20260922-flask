import os
from hmac import compare_digest

from flask import Flask, jsonify, request
from flask_smorest import Api, Blueprint

app = Flask(__name__)

app.config.from_mapping(
    API_TITLE="Task API",
    API_VERSION="1.0",
    OPENAPI_VERSION="3.0.3",
    OPENAPI_URL_PREFIX="/",
    OPENAPI_JSON_PATH="openapi.json",
    OPENAPI_SWAGGER_UI_PATH="docs",
    OPENAPI_SWAGGER_UI_URL="https://cdn.jsdelivr.net/npm/swagger-ui-dist/",
    OPENAPI_REDOC_PATH="redoc",
    OPENAPI_REDOC_URL="https://cdn.jsdelivr.net/npm/redoc@2/bundles/redoc.standalone.js",
    API_SPEC_OPTIONS={
        "components": {
            "securitySchemes": {"BearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "API token"}}
        },
        "security": [{"BearerAuth": []}],
    },
    AUTH_TOKEN=os.environ.get("TASK_API_TOKEN", "example-token"),
)

api = Api(app)
public = Blueprint("public", __name__)
task_routes = Blueprint("tasks", __name__, url_prefix="/tasks", description="Create and manage tasks.")


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


@public.route("/", methods=["GET"])
def welcome():
    return jsonify({"message": "Welcome to the Task API"})


@app.before_request
def require_auth_token():
    """Require a bearer token for API endpoints, excluding public docs."""
    if request.endpoint in (None, "public.welcome") or request.endpoint.startswith("api-docs."):
        return None

    scheme, _, token = request.headers.get("Authorization", "").partition(" ")
    if scheme != "Bearer" or not compare_digest(token, app.config["AUTH_TOKEN"]):
        return jsonify({"error": "A valid bearer token is required"}), 401

    return None


@task_routes.route("", methods=["GET"])
def get_tasks():
    return jsonify(list(tasks.values()))


@task_routes.route("/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = tasks.get(task_id)
    if task is None:
        return jsonify({"error": "Task not found"}), 404

    return jsonify(task)


@task_routes.route("", methods=["POST"])
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


@task_routes.route("/<int:task_id>", methods=["PATCH"])
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


@task_routes.route("/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    if task_id not in tasks:
        return jsonify({"error": "Task not found"}), 404

    del tasks[task_id]
    return "", 204


api.register_blueprint(public)
api.register_blueprint(task_routes)


def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()
