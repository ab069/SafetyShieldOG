from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Set

router = APIRouter()
active_connections: Set[WebSocket] = set()

@router.websocket("/ws/hse")
async def hse_websocket(websocket: WebSocket):
    await websocket.accept()
    active_connections.add(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        active_connections.discard(websocket)

async def broadcast_hse_event(event: dict):
    for conn in active_connections.copy():
        try:
            await conn.send_json(event)
        except Exception:
            active_connections.discard(conn)
