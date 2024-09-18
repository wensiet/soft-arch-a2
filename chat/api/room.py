from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from chat.service.room import RoomService

router = APIRouter(prefix="/room", tags=["Rooms"])

room_service = RoomService()


@router.websocket("/websocket")
async def websocket_endpoint(websocket: WebSocket):
    author = await room_service.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await room_service.send_message(data, author)
    except WebSocketDisconnect:
        await room_service.disconnect(websocket, author)


@router.get("/message_count")
async def messages_count():
    return {"message_count": room_service.get_message_count()}
