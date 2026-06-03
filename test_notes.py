import json
import zmq


def send_request(socket, payload):
    """
    Helper function to send request and print response.
    """

    socket.send_string(json.dumps(payload))
    response = socket.recv_string()

    print(json.dumps(json.loads(response), indent=4))
    print("-" * 40)


def main():

    context = zmq.Context()
    socket = context.socket(zmq.REQ)

    # Connect to Notes microservice
    socket.connect("tcp://localhost:5557")

    # Create note
    print("Creating note...")
    send_request(socket, {
        "action": "create_note",
        "app_name": "TaskManager",
        "user_id": "123",
        "title": "Study Reminder",
        "content": "Finish CS assignment before Friday"
    })

    # Get all notes
    print("Getting notes...")
    send_request(socket, {
        "action": "get_notes",
        "user_id": "123"
    })

    # Delete note 
    print("Deleting note...")
    send_request(socket, {
        "action": "delete_note",
        "note_id": 1
    })

    # Confirm deletion
    print("Final check...")
    send_request(socket, {
        "action": "get_notes",
        "user_id": "123"
    })


if __name__ == "__main__":
    main()