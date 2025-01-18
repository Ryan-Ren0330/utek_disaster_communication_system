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
    print(data) # for debugging
    # save the data
    save_form_data(data)
    return jsonify({"message": "Form submitted successfully!", "status": "success"})


@app.route("/api/fire_reports", methods=["GET"])
def get_fire_reports():
    data_path = "../data/form_data.json"
    with open(data_path, "r") as f:
        fire_reports = json.load(f)
    return jsonify(fire_reports)


if __name__ == "__main__":
    app.run(debug=True, port=5000)