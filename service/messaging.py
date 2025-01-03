from fastapi import FastAPI, WebSocket, WebSocketDisconnect




active_connections = {}


@router.websocket("/ws/{student_id}/{professor_id}")
async def websocket_endpoint(websocket: WebSocket, student_id, professor_id):

    await websocket.accept()
    connection_id = f"{student_id}_{professor_id}"
    active_connections[connection_id] = websocket

    try:
        while True:
            data = await websocket.receive_text()
            # Process incoming data here as needed

            # For demonstration, let's broadcast the received message to other connected users
            for conn_id, conn in active_connections.items():
                if conn_id != connection_id:
                    await conn.send_text(f"Professor {professor_id} said: {data}")

    except WebSocketDisconnect:
        del active_connections[connection_id]


@router.post("/send_message/{student_id}/{professor_id}")
async def send_message(student_id, professor_id, message: str):
    connection_id = f"{student_id}_{professor_id}"
    if connection_id in active_connections:
        websocket = active_connections[connection_id]
        await websocket.send_text(f"Student {student_id} said: {message}")
        return {"message": "Message sent successfully"}

    return {"message": "Student or Professor not connected"}


@router.get("/receive_messages/{student_id}/{professor_id}")
async def receive_messages(student_id, professor_id):
    connection_id = f"{student_id}_{professor_id}"
    if connection_id in active_connections:
        websocket = active_connections[connection_id]
        messages = []
        try:
            while True:
                data = await websocket.receive_text()
                messages.append(data)
        except WebSocketDisconnect:
            return {"messages": messages}
    else:
        return {"message": "Student or Professor not connected"}
