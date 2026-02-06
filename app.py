from flask import Flask, request, jsonify, send_from_directory
import json, os

app = Flask(__name__, static_folder="static")

STATE_FILE = "state.json"

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.get("/state")
def get_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return jsonify(json.load(f))
    return jsonify({})

@app.post("/state")
def save_state():
    data = request.get_json(force=True)
    with open(STATE_FILE, "w") as f:
        json.dump(data, f, indent=2)
    return {"ok": True}

@app.post("/reset")
def reset_state():
    if os.path.exists(STATE_FILE):
        os.remove(STATE_FILE)
    return {"ok": True}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
