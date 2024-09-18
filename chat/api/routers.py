from fastapi import FastAPI
from starlette.responses import HTMLResponse

from chat import settings
from chat.api.room import router as room_router
from chat.service.room import RoomService

app = FastAPI()
app.include_router(room_router)

room_service = RoomService()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://{web_socket_host}/room/websocket");
            ws.onmessage = function(event) {{
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                var br = document.createElement('br')
                message.appendChild(content)
                messages.appendChild(message)
                messages.appendChild(br)
            }};
            function sendMessage(event) {{
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }}
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html.format(web_socket_host=settings.WEBSOCKET_HOST))
