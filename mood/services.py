mood_db = {}  # In-memory storage for demonstration

def add_mood_entry(child_id, mood):
    if child_id not in mood_db:
        mood_db[child_id] = []
    mood_db[child_id].append(mood)

def get_mood_entries(child_id):
    return mood_db.get(child_id, [])
