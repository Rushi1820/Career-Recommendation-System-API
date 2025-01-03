from fastapi import FastAPI, WebSocket, WebSocketDisconnect

import logging

from fastapi import APIRouter


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s:%(message)s")

file_handler = logging.FileHandler("logs//user.log")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

router = APIRouter(tags=["Messaging"], prefix="/msg")


active_connections = {}
messages_store = {}


@router.websocket("/ws/{student_id}/{professor_id}")
async def websocket_endpoint(websocket: WebSocket, student_id:str, professor_id:str):
    await websocket.accept()
    connection_id = f"{student_id}_{professor_id}"
    active_connections[connection_id] = websocket

    try:
        while True:
            data = await websocket.receive_text()
            current_time = datetime.now()
            if connection_id in messages_store:
                messages_store[connection_id].append((current_time, data))
            else:
                messages_store[connection_id] = [(current_time, data)]

            for conn_id, conn in active_connections.items():
                if conn_id != connection_id:
                    await conn.send_text(f"Professor {professor_id} said: {data}")

    except WebSocketDisconnect:
        del active_connections[connection_id]


@router.post("/send_message/{student_id}/{professor_id}")
async def send_message(student_id: str, professor_id:str, message: str):
    connection_id = f"{student_id}_{professor_id}"
    if connection_id in active_connections:
        websocket = active_connections[connection_id]
        await websocket.send_text(f"Student {student_id} said: {message}")

        current_time = datetime.now()
        if connection_id in messages_store:
            messages_store[connection_id].append((current_time, message))
        else:
            messages_store[connection_id] = [(current_time, message)]

        return {"message": "Message sent successfully"}

    return {"message": "Student or Professor not connected"}


@router.get("/receive_messages/{student_id}/{professor_id}")
async def receive_messages(student_id: str, professor_id: str):
    connection_id = f"{student_id}_{professor_id}"
    if connection_id in messages_store:
        current_time = datetime.now()
        twenty_four_hours_ago = current_time - timedelta(hours=24)
        recent_messages = [
            {"timestamp": str(timestamp), "message": message}
            for timestamp, message in messages_store[connection_id]
            if timestamp >= twenty_four_hours_ago
        ]
        return {"messages": recent_messages}

    return {"message": "No messages in the last 24 hours"}