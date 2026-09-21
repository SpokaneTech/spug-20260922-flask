from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/", methods=["GET"])
def welcome():
    return jsonify({"message": "Welcome to the Task API"})


def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()
