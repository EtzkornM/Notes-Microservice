A. Notes-Microservice

The Notes Microservice allows applications such as task managers and productivity apps to create, retrieve, and delete user notes. It provides a simple way for applications to store additional information related to tasks, events, or general reminders. The microservice communicates using JSON messages and returns either note data or error messages.


B. To programmatically REQUEST data from the microservice:

A program connects to it using ZeroMQ. It sends a message in JSON format that includes the required information:

- app_name: Name of the application making the request
- user_id: Unique identifier for the user
- action: The operation to perform on the notes service

Supported actions:
- create_note
- get_notes
- delete_note

Depending on the action, additional fields may be required:

create_note requires:
- title: Title of the note
- content: Content of the note
  
get_notes requires:
- user_id
  
delete_note requires:
- note_id

The microservice uses this information to perform the requested operation and returns either a success response or an error message.

The service returns an error message if:
- app_name is missing
- user_id is missing (when required)
- action is missing or invalid
- required fields for an action are missing
- note_id does not exist (for delete operations)

Example Request:

```
{
    "action": "create_note",
    "app_name": "TaskManager",
    "user_id": "123",
    "title": "Study Reminder",
    "content": "Finish CS assignment before Friday"
}
```

Explanation:

1. ZeroMQ context and REQ socket are created
2. The client connects to the microservice at tcp://localhost:5557
3. JSON request is constructed with the required fields
4. The request is converted to a JSON string using json.dumps() and sent to the microservice

C. To programmatically RECEIVE data from the microservice:

After sending a request, the program waits for a response from the microservice. The response comes back as a JSON string. The program then converts it into a Python dictionary so it can be used or printed.

Example Response Code:

```
response = socket.recv_string()
data = json.loads(response)

print(data)
```

Example Successful Response (Create Note):

```
{
    "message": "Note created",
    "note": {
        "note_id": 1,
        "app_name": "TaskManager",
        "user_id": "123",
        "title": "Study Reminder",
        "content": "Finish CS assignment before Friday",
        "timestamp": "2026-06-03 12:25:48"
    }
}
```

Example Successful Response (Get Notes):

```
{
    "notes": [
        {
            "note_id": 1,
            "app_name": "TaskManager",
            "user_id": "123",
            "title": "Study Reminder",
            "content": "Finish CS assignment before Friday",
            "timestamp": "2026-06-03 12:25:48"
        }
    ]
}
```

Example Error Response:
```
{
    "message": "Note not found"
}
```

```
{
    "message": "Missing required field: content"
}
```

Explanation:
1. recv_string() waits for a response from the microservice
2. json.loads() converts the JSON string into a Python dictionary
3. The application can access returned values using dictionary keys such as notes, note, or message
