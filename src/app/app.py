from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/", methods=["GET"])
def get_item():
    return jsonify({"status": "active"})


def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()
