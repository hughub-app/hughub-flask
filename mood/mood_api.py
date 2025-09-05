from flask_smorest import Blueprint
from flask import request, jsonify
from models import MoodLog, Children
from extension import db
from datetime import datetime
from schemas.mood_logs import (
    MoodLog as MoodLogSchema,
    CreateMoodLog,
    MoodLogsRangeQuery,
    UpdateMoodLog,
)
from schemas.common import MessageSchema

blp = Blueprint("mood_logs", __name__, url_prefix="/mood_logs",
                description="Mood Logs API")

# ---------------------------
# Create Mood Log
# ---------------------------
@blp.route("/", methods=["POST"])
@blp.arguments(CreateMoodLog())  # request schema
@blp.response(201, MoodLogSchema())  # response schema
@blp.doc(description="Create a new mood log")
def create_mood_log(payload):
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
    if not Children.query.get(payload["child_id"]):
        return {"error": "Child not found"}, 404
    # if not (child_id and mood):
    #     return jsonify({"error": "Missing required fields"}), 400

    mood_log = MoodLog(
        child_id=payload["child_id"],
        mood=payload["mood"],
        created_at=datetime.now()
    )
    if "notes" in payload:
        mood_log.notes = payload.get("notes")

    db.session.add(mood_log)
    db.session.commit()
    
    return mood_log, 201

# ---------------------------
# Read All Mood Logs
# ---------------------------
@blp.route("/", methods=["GET"])
@blp.response(200, MoodLogSchema(many=True))  # response schema (array of MoodLog)
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
    # child_id = request.args.get("child_id", type=int)
    # mood = request.args.get("mood", type=str)

    query = MoodLog.query
    # if child_id:
    #     query = query.filter(MoodLog.child_id == child_id)
    # if mood:
    #     query = query.filter(MoodLog.mood.ilike(f"%{mood}%"))

    mood_logs = query.all()
    return mood_logs


# ---------------------------
# Read Mood Log Based on Child ID
# ---------------------------
@blp.route("/<int:child_id>", methods=["GET"])
@blp.doc(
    description="Get a single mood log by using the child ID",
    parameters=[
        {
            "in": "path",
            "name": "child_id",
            "schema": {"type": "integer"},
            "required": True,
            "description": "ID of the child to fetch the mood log for"
        }
    ]
)
@blp.response(200, MoodLogSchema(many=True))  # response schema (array of MoodLog)
def get_mood_log(child_id):
    """
    Get a mood log by child ID
    ---
    parameters:
      - in: path
        name: mood_log_id
        schema:
          type: integer
        required: true
        description: ID of the child 
    responses:
      200:
        description: Mood log object
      404:
        description: Mood log not found
    """
    if not Children.query.get(child_id):
        return jsonify({"error": "Child not found"}), 404
    mood_logs = MoodLog.query.filter(MoodLog.child_id == child_id).all()

    return mood_logs


# ---------------------------
# Update Mood Log
# ---------------------------
@blp.route("/<int:mood_log_id>", methods=["PUT"])
@blp.arguments(UpdateMoodLog())  # request schema (partial)
@blp.response(200, MoodLogSchema())  # response schema
@blp.doc(description="Update a mood log by ID")
def update_mood_log(payload, mood_log_id):
    mood = payload.get("mood")
    notes = payload.get("notes")

    mood_log = MoodLog.query.get_or_404(mood_log_id)

    if mood:
        mood_log.mood = mood
    if notes is not None:
        mood_log.notes = notes

    db.session.commit()

    return mood_log


# ---------------------------
# Delete Mood Log
# ---------------------------
@blp.route("/<int:mood_log_id>", methods=["DELETE"])
@blp.response(200, MessageSchema())  # response schema
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
    return {"message": "Mood log deleted"}


@blp.route("/latest/<int:child_id>", methods=["GET"])
@blp.response(200, MoodLogSchema())  # response schema
@blp.doc(description="Get the latest mood log for a specific child")
def get_latest_mood(child_id):
    # ensure the child exists
    print(child_id)
    child = Children.query.get(child_id)
    if not child:
        return jsonify({"error": "Child not found"}), 404

    # get the latest mood log for the child
    mood_log = (
        MoodLog.query
        .filter(MoodLog.child_id == child_id)
        .order_by(MoodLog.created_at.desc())
        .first()
    )

    if not mood_log:
        return {"error": "No mood logs found for this child"}, 404

    return mood_log


@blp.route("/range/<int:child_id>", methods=["GET"])
@blp.arguments(MoodLogsRangeQuery, location="query")
@blp.response(200, MoodLogSchema(many=True))  # response schema (array of MoodLog)
def get_moods_by_time_range(query_args, child_id):       # <-- order matters
    start_time = query_args["start"]
    end_time = query_args["end"]
    
    # check if the child exists
    child = Children.query.get(child_id)
    if not child:
        return jsonify({"error": "Child not found"}), 404

    mood_logs = (
        MoodLog.query
        .filter(
            MoodLog.child_id == child_id,
            MoodLog.created_at >= start_time,
            MoodLog.created_at <= end_time
        )
        .order_by(MoodLog.created_at.asc())
        .all()
    )

    if not mood_logs:
        return {"error": "No mood logs found in the specified range"}, 404

    return mood_logs
