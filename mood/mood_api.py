from flask_smorest import Blueprint
from flask import request, jsonify
from .services import add_mood_entry, get_mood_entries

blp = Blueprint("mood", __name__, url_prefix="/mood",
                description="Children Emotion API")

@blp.route("/add", methods=["POST"])
def add_mood():
    data = request.get_json()
    child_id = data.get("child_id")
    mood = data.get("mood")

    add_mood_entry(child_id, mood)
    return jsonify({"message": "Mood entry added", "child_id": child_id, "mood": mood})

@blp.route("/on", methods=["GET"])
def start():
    return jsonify({"message": "Mood API is operational"})

@blp.route("/history/<int:child_id>", methods=["GET"])
def get_mood_history(child_id):
    moods = get_mood_entries(child_id)
    return jsonify({"child_id": child_id, "mood_history": moods})
