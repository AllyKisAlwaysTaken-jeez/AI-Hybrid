from flask import Flask, render_template, request, jsonify
import json, os

app = Flask(__name__)

MEMORY_FILE = "memory.json"



# Helpers

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {"user": {}, "site": {}, "assistant_notes": {}}
    with open(MEMORY_FILE) as f:
        return json.load(f)


def save_memory(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)



# Pages

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/assistant")
def assistant():
    return render_template("assistant.html")


@app.route("/preview")
def preview():
    memory = load_memory()
    return render_template("preview.html", memory=memory)



# API: from index.html

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    memory = load_memory()

    # Save user info
    memory["user"]["industry"] = data.get("industry", "")
    memory["user"]["style"] = data.get("style", "")
    memory["user"]["goals"] = data.get("goals", "")

    # competitors: split by comma
    competitors_raw = data.get("competitors", "")
    memory["user"]["competitors"] = [
        c.strip() for c in competitors_raw.split(",") if c.strip()
    ]

    save_memory(memory)

    # Create a response for the UI
    response = {
        "message": f"Got it! I'll build your portfolio using a {memory['user']['style']} design for the {memory['user']['industry']} industry. Your goal is: {memory['user']['goals']}."
    }

    return jsonify(response)


# API: assistant editing tool
@app.route("/api/update-site", methods=["POST"])
def update_site():
    memory = load_memory()
    updates = request.json.get("updates", {})

    for key, value in updates.items():
        if key == "skills":
            memory["site"]["skills"] = [s.strip() for s in value.split(",")]
        else:
            memory["site"][key] = value

    save_memory(memory)

    return jsonify({"message": "Changes applied!"})

if __name__ == "__main__":
    app.run(debug=True)
