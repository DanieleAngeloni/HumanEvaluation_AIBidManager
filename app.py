from flask import Flask, request, jsonify, send_from_directory, abort
import json, os

app = Flask(__name__, static_folder="static")

STATE_FILE = "state.json"
PASSWORD = os.environ.get("APP_PASSWORD", "valutazione2026")

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.post("/login")
def login():
    data = request.get_json(force=True)
    if data.get("password") == PASSWORD:
        return {"ok": True}
    abort(401)

@app.get("/state")
def get_state():
    if not authorized():
        abort(401)
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return jsonify(json.load(f))
    return jsonify({})

@app.post("/state")
def save_state():
    if not authorized():
        abort(401)
    data = request.get_json(force=True)
    with open(STATE_FILE, "w") as f:
        json.dump(data, f, indent=2)
    return {"ok": True}

@app.post("/reset")
def reset_state():
    if not authorized():
        abort(401)
    if os.path.exists(STATE_FILE):
        os.remove(STATE_FILE)
    return {"ok": True}

def authorized():
    return request.headers.get("X-Auth") == PASSWORD

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
