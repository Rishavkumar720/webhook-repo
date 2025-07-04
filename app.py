from flask import Flask, request, render_template
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import datetime

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["webhookDB"]
collection = db["events"]

@app.route("/", methods=["GET"])
def home():
    """Home route"""
    return "Flask server is running!", 200

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    """Webhook to receive GitHub events"""
    if request.method == "GET":
        return "Webhook endpoint is live!", 200

    if request.method == "POST":
        payload = request.json
        event_type = request.headers.get("X-GitHub-Event")

        try:
            timestamp = datetime.utcnow()

            if event_type == "push":
                author = payload["head_commit"]["author"]["name"]
                to_branch = payload["ref"].split("/")[-1]

                data = {
                    "type": "push",
                    "author": author,
                    "to_branch": to_branch,
                    "timestamp": timestamp,
                }

            elif event_type == "pull_request":
                action = payload.get("action")
                pr = payload.get("pull_request", {})

                if action == "opened":
                    author = pr["user"]["login"]
                    from_branch = pr["head"]["ref"]
                    to_branch = pr["base"]["ref"]

                    data = {
                        "type": "pull_request",
                        "author": author,
                        "from_branch": from_branch,
                        "to_branch": to_branch,
                        "timestamp": timestamp,
                    }

                elif action == "closed" and pr.get("merged"):
                    author = pr["merged_by"]["login"]
                    from_branch = pr["head"]["ref"]
                    to_branch = pr["base"]["ref"]

                    data = {
                        "type": "merge",
                        "author": author,
                        "from_branch": from_branch,
                        "to_branch": to_branch,
                        "timestamp": timestamp,
                    }
                else:
                    return {"message": "Ignored pull_request action"}, 200
            else:
                return {"message": f"Ignored event type: {event_type}"}, 200

            # Insert into MongoDB
            collection.insert_one(data)
            print("Event saved:", data)
            return {"message": "Event received and stored!"}, 200

        except Exception as e:
            print("❌ Error:", str(e))
            return {"error": str(e)}, 400

@app.route("/dashboard", methods=["GET"])
def dashboard():
    """Dashboard displaying recent events"""
    events = list(collection.find().sort("timestamp", -1).limit(10))
    for event in events:
        event["timestamp"] = event["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
    return render_template("dashboard.html", events=events)

if __name__ == "__main__":
    app.run(debug=True)
