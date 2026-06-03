import json
from datetime import datetime
import zmq
import os


NOTES_FILE = "notes.json"


def load_notes():
    """
    Load notes from JSON file.
    """

    if not os.path.exists(NOTES_FILE):
        return []

    with open(NOTES_FILE, "r") as file:
        return json.load(file)


def save_notes(notes):
    """
    Save notes to JSON file.
    """

    with open(NOTES_FILE, "w") as file:
        json.dump(notes, file, indent=4)


def generate_note_id(notes):
    """
    Generate a unique note ID.
    """

    if not notes:
        return 1

    return max(note["note_id"] for note in notes) + 1


def create_note(data):
    """
    Create a new note.
    """

    app_name = data.get("app_name")
    user_id = data.get("user_id")
    title = data.get("title")
    content = data.get("content")

    if not app_name:
        return {"message": "Missing app_name"}

    if not user_id:
        return {"message": "Missing user_id"}

    if not title:
        return {"message": "Missing title"}

    if not content:
        return {"message": "Missing content"}

    notes = load_notes()

    note = {
        "note_id": generate_note_id(notes),
        "app_name": app_name,
        "user_id": user_id,
        "title": title,
        "content": content,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    notes.append(note)
    save_notes(notes)

    return {
        "message": "Note created",
        "note": note
    }


def get_notes(data):
    """
    Retrieve all notes for a user.
    """

    user_id = data.get("user_id")

    if not user_id:
        return {"message": "Missing user_id"}

    notes = load_notes()

    user_notes = [
        note for note in notes
        if note["user_id"] == user_id
    ]

    return {
        "notes": user_notes
    }


def delete_note(data):
    """
    Delete a note by ID.
    """

    note_id = data.get("note_id")

    if note_id is None:
        return {"message": "Missing note_id"}

    notes = load_notes()

    for note in notes:
        if note["note_id"] == note_id:
            notes.remove(note)
            save_notes(notes)
            return {"message": "Note deleted"}

    return {"message": "Note not found"}


def main():
    """
    Start Notes Microservice using ZeroMQ.
    """

    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5557")

    print("Notes microservice running on tcp://localhost:5557")

    while True:

        request = socket.recv_string()
        data = json.loads(request)

        action = data.get("action")

        if action == "create_note":
            response = create_note(data)

        elif action == "get_notes":
            response = get_notes(data)

        elif action == "delete_note":
            response = delete_note(data)

        else:
            response = {
                "message": "Unsupported action"
            }

        socket.send_string(json.dumps(response))


if __name__ == "__main__":
    main()