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
@blp.doc(
    description="Create a new mood log",
    requestBody={
        "required": True,
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "child_id": {"type": "integer"},
                        "mood": {"type": "string"},
                        "notes": {"type": "string"}
                    },
                    "required": ["child_id", "mood"]
                }
            }
        }
    },
    responses={
        201: {"description": "Mood log created successfully"},
        400: {"description": "Missing required fields"}
    }
)
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
    # child_id = request.args.get("child_id", type=int)
    # mood = request.args.get("mood", type=str)

    query = MoodLog.query
    # if child_id:
    #     query = query.filter(MoodLog.child_id == child_id)
    # if mood:
    #     query = query.filter(MoodLog.mood.ilike(f"%{mood}%"))

    mood_logs = query.all()
    result = [m.to_dict() for m in mood_logs]
    return jsonify(result)


# ---------------------------
# Read Mood Log Based on Child ID
# ---------------------------
@blp.route("/<int:child_id>", methods=["GET"])
@blp.doc(description="Get a single mood log by using the child ID")
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
    
    result = [m.to_dict() for m in mood_logs]

    return jsonify({
        "child_id": child_id,
        "mood_logs": result
    })


# ---------------------------
# Update Mood Log
# ---------------------------
@blp.route("/<int:mood_log_id>", methods=["PUT"])
@blp.doc(
    description="Update a mood log by ID",
    parameters=[
        {
            "in": "path",
            "name": "mood_log_id",
            "schema": {"type": "integer"},
            "required": True,
            "description": "ID of the mood log to update"
        },
        {
            "in": "query",
            "name": "mood",
            "schema": {"type": "string"},
            "required": False,
            "description": "New mood value"
        },
        {
            "in": "query",
            "name": "notes",
            "schema": {"type": "string"},
            "required": False,
            "description": "New notes for the mood log"
        }
    ],
    responses={
        200: {"description": "Mood log updated successfully"},
        404: {"description": "Mood log not found"}
    }
)
def update_mood_log(mood_log_id):
    mood = request.args.get("mood")
    notes = request.args.get("notes")

    mood_log = MoodLog.query.get_or_404(mood_log_id)

    if mood:
        mood_log.mood = mood
    if notes is not None:
        mood_log.notes = notes

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


@blp.route("/latest/<int:child_id>", methods=["GET"])
@blp.doc(
    description="Get the latest mood log for a specific child",
    parameters=[
        {
            "in": "path",
            "name": "child_id",
            "schema": {"type": "integer"},
            "required": True,
            "description": "ID of the child to fetch the latest mood log for"
        }
    ],
    responses={
        200: {
            "description": "Latest mood log found",
            "content": {
                "application/json": {
                    "example": {
                        "mood_log": {
                            "mood_log_id": 10,
                            "child_id": 1,
                            "mood": "Happy",
                            "notes": "Had fun at school",
                            "created_at": "2025-09-03T13:00:00"
                        }
                    }
                }
            }
        },
        404: {"description": "Child not found or no mood logs available"}
    }
)
def get_latest_mood(child_id):
    # ensure the child exists
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
        return jsonify({"error": "No mood logs found for this child"}), 404

    return jsonify({"mood_log": mood_log.to_dict()})


from datetime import datetime

@blp.route("/range/<int:child_id>", methods=["GET"])
@blp.doc(
    description="Get all mood logs for a child between two timestamps",
    parameters=[
        {
            "in": "path",
            "name": "child_id",
            "schema": {"type": "integer"},
            "required": True,
            "description": "ID of the child to fetch mood logs for"
        },
        {
            "in": "query",
            "name": "start",
            "schema": {"type": "string", "format": "date-time"},
            "required": True,
            "description": "Start timestamp (ISO format, e.g. 2025-09-01T00:00:00)"
        },
        {
            "in": "query",
            "name": "end",
            "schema": {"type": "string", "format": "date-time"},
            "required": True,
            "description": "End timestamp (ISO format, e.g. 2025-09-03T23:59:59)"
        }
    ],
    responses={
        200: {
            "description": "Mood logs found",
            "content": {
                "application/json": {
                    "example": {
                        "mood_logs": [
                            {
                                "mood_log_id": 15,
                                "child_id": 1,
                                "mood": "Happy",
                                "notes": "Played outside",
                                "created_at": "2025-09-02T10:00:00"
                            },
                            {
                                "mood_log_id": 16,
                                "child_id": 1,
                                "mood": "Tired",
                                "notes": "After soccer practice",
                                "created_at": "2025-09-02T18:30:00"
                            }
                        ]
                    }
                }
            }
        },
        400: {"description": "Missing or invalid parameters"},
        404: {"description": "Child not found or no mood logs in the range"}
    }
)
def get_moods_by_time_range(child_id):
    # check if the child exists
    child = Children.query.get(child_id)
    if not child:
        return jsonify({"error": "Child not found"}), 404

    start_str = request.args.get("start")
    end_str = request.args.get("end")

    if not start_str or not end_str:
        return jsonify({"error": "Missing start or end timestamp"}), 400

    try:
        start_time = datetime.fromisoformat(start_str)
        end_time = datetime.fromisoformat(end_str)
    except ValueError:
        return jsonify({"error": "Invalid timestamp format, use ISO format"}), 400

    # query mood logs in the specified time range
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
        return jsonify({"error": "No mood logs found in the specified range"}), 404

    return jsonify({"mood_logs": [log.to_dict() for log in mood_logs]})
