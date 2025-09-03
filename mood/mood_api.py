from flask_smorest import Blueprint
from flask import request, jsonify
from models import MoodLog, Children
from extension import db
from datetime import datetime

blp = Blueprint("mood", __name__, url_prefix="/mood_logs",
                description="Mood Logs API")

# ---------------------------
# Create Mood Log
# ---------------------------
@blp.route("/on", methods=["GET"])
def start():
    return jsonify({"message": "Mood API is operational"})

@blp.route("/", methods=["POST"])
@blp.doc(description="Create a new mood log")
def create_mood_log():
    """
    Create a new mood log
    ---
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              child_id:
                type: integer
              mood:
                type: string
              notes:
                type: string
    responses:
      201:
        description: Mood log created successfully
    """
    data = request.get_json()
    child_id = data.get("child_id")
    mood = data.get("mood")
    if not (child_id and mood):
        return jsonify({"error": "Missing required fields"}), 400
    
    mood_log = MoodLog(
        child_id=data["child_id"],
        mood=data["mood"],
        created_at=datetime.now()
    )
    if "notes" in data:
        mood_log.notes = data.get("notes")
        
    db.session.add(mood_log)
    db.session.commit()
    return jsonify({"message": "Mood log created", "mood_log": mood_log.to_dict()}), 201


# ---------------------------
# Read All Mood Logs
# ---------------------------
@blp.route("/", methods=["GET"])
@blp.doc(description="Get all mood logs with optional filters")
def get_all_mood_logs():
    """
    Get all mood logs
    ---
    parameters:
      - in: query
        name: child_id
        schema:
          type: integer
        required: false
        description: Filter by child ID
      - in: query
        name: mood
        schema:
          type: string
        required: false
        description: Filter by mood
    responses:
      200:
        description: List of mood logs
    """
    child_id = request.args.get("child_id", type=int)
    mood = request.args.get("mood", type=str)

    query = MoodLog.query
    if child_id:
        query = query.filter(MoodLog.child_id == child_id)
    if mood:
        query = query.filter(MoodLog.mood.ilike(f"%{mood}%"))

    mood_logs = query.all()
    result = [m.to_dict() for m in mood_logs]
    return jsonify(result)


# ---------------------------
# Read One Mood Log
# ---------------------------
@blp.route("/<int:mood_log_id>", methods=["GET"])
@blp.doc(description="Get a single mood log by ID")
def get_mood_log(mood_log_id):
    """
    Get a mood log by ID
    ---
    parameters:
      - in: path
        name: mood_log_id
        schema:
          type: integer
        required: true
        description: ID of the mood log
    responses:
      200:
        description: Mood log object
      404:
        description: Mood log not found
    """
    mood_log = MoodLog.query.get_or_404(mood_log_id)
    return jsonify(mood_log.to_dict())


# ---------------------------
# Update Mood Log
# ---------------------------
@blp.route("/<int:mood_log_id>", methods=["PUT"])
@blp.doc(description="Update a mood log by ID")
def update_mood_log(mood_log_id):
    """
    Update a mood log
    ---
    parameters:
      - in: path
        name: mood_log_id
        schema:
          type: integer
        required: true
        description: ID of the mood log
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              mood:
                type: string
              notes:
                type: string
    responses:
      200:
        description: Mood log updated successfully
      404:
        description: Mood log not found
    """
    data = request.get_json()
    mood_log = MoodLog.query.get_or_404(mood_log_id)

    mood_log.mood = data.get("mood", mood_log.mood)
    mood_log.notes = data.get("notes", mood_log.notes)
    db.session.commit()

    return jsonify({"message": "Mood log updated", "mood_log": mood_log.to_dict()})


# ---------------------------
# Delete Mood Log
# ---------------------------
@blp.route("/<int:mood_log_id>", methods=["DELETE"])
@blp.doc(description="Delete a mood log by ID")
def delete_mood_log(mood_log_id):
    """
    Delete a mood log
    ---
    parameters:
      - in: path
        name: mood_log_id
        schema:
          type: integer
        required: true
        description: ID of the mood log
    responses:
      200:
        description: Mood log deleted successfully
      404:
        description: Mood log not found
    """
    mood_log = MoodLog.query.get_or_404(mood_log_id)
    db.session.delete(mood_log)
    db.session.commit()
    return jsonify({"message": "Mood log deleted"})
