from flask import Flask, request, jsonify
import json

app = Flask(__name__)


def save_form_data(data):
    # save the data
    data_path = "../data/form_data.json"
    with open(data_path, "r") as f:
        form_data = json.load(f)
    form_data.append(data)
    with open(data_path, "w") as f:
        json.dump(form_data, f, indent=4)


@app.route("/api/form", methods=["POST"])
def submit_form():
    data = request.json
    # save the data
    save_form_data(data)
    return jsonify({"message": "Form submitted successfully!", "status": "success"})


@app.route("/api/fire_reports", methods=["GET"])
def get_fire_reports():
    data_path = "../data/form_data.json"
    with open(data_path, "r") as f:
        fire_reports = json.load(f)
    return jsonify(fire_reports)


@app.route("/api/add_history", methods=["POST"])
def add_chat_history():
    data = request.json
    # save the data
    data_path = "../data/form_data.json"
    with open(data_path, "r") as f:
        form_data = json.load(f)
    for report in form_data:
        if report["user_id"] == data["user_id"]:
            report["chat_history"].append(data["chat"])
            break
    with open(data_path, "w") as f:
        json.dump(form_data, f, indent=4)
    return jsonify({"message": "Chat history added successfully!", "status": "success"})


@app.route("/api/fetch_chat_history", methods=["POST"])
def fetch_chat_history():
    data = request.json
    data_path = "../data/form_data.json"
    with open(data_path, "r") as f:
        form_data = json.load(f)
    chat_history = []
    for report in form_data:
        if report["user_id"] == data["user_id"]:
            chat_history = report["chat_history"]
            break
    return jsonify(chat_history)


if __name__ == "__main__":
    app.run(debug=True, port=5000)