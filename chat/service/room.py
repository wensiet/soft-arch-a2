import datetime
import random
import uuid
from typing import Type

from starlette.websockets import WebSocket

name_alphabet = {
    "colors": [
        "red",
        "green",
        "blue",
        "yellow",
        "orange",
        "purple",
        "pink",
        "brown",
        "black",
        "white",
    ],
    "animals": [
        "dog",
        "cat",
        "bird",
        "fish",
        "rabbit",
        "hamster",
        "turtle",
        "horse",
        "parrot",
        "spider",
    ],
    "byname": [
        "speedy",
        "bobik",
        "smew",
        "shrek",
        "ralph",
        "buddy",
        "dobby",
        "dumbo",
        "bambi",
    ]
}

TIME_FORMAT = "%Y-%m-%d %H:%M"


def _generate_name() -> str:
    color = random.choice(name_alphabet["colors"])
    animal = random.choice(name_alphabet["animals"])
    byname = random.choice(name_alphabet["byname"])
    return f"{color.capitalize()} {animal.capitalize()} {byname.capitalize()}"


class RoomService:
    _instance = None

    def __new__(cls: "Type[RoomService]", *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(RoomService, cls).__new__(cls)
            cls._instance.active_connections: list[WebSocket] = []
            cls._instance.message_count: int = 0
            cls._instance.occupied_names: list[str] = []
        return cls._instance

    def _generate_unique_name(self) -> str:
        name = _generate_name()
        max_tries = 100
        while name in self.occupied_names:
            name = _generate_name()
            max_tries -= 1
            if max_tries == 0:
                name = str(uuid.uuid4())
                break
        self.occupied_names.append(name)
        return name

    async def connect(self, websocket: WebSocket) -> str:
        await websocket.accept()
        self.active_connections.append(websocket)
        user_id = self._generate_unique_name()
        await self.send_message(websocket, f"User {user_id} joined the chat")
        return user_id

    async def disconnect(self, websocket: WebSocket, author: str):
        self.active_connections.remove(websocket)
        self.occupied_names.remove(author)
        await self.send_message(websocket, f"User {author} left the chat")

    async def send_message(self, websocket: WebSocket, message: str, author: str | None = None):
        self.message_count += 1
        for connection in self.active_connections:
            if connection != websocket:
                if author:
                    await connection.send_text(f"{datetime.datetime.now().strftime(TIME_FORMAT)} {author}: {message}")
                else:
                    await connection.send_text(f"{datetime.datetime.now().strftime(TIME_FORMAT)} {message}")

    def get_message_count(self) -> int:
        return self.message_count
