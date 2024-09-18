from fastapi import FastAPI
from starlette.responses import HTMLResponse

from chat.api.room import router as room_router
from chat.service.room import RoomService

app = FastAPI()
app.include_router(room_router)

room_service = RoomService()

html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Anonymous Chat</title>
    <style>
        /* Global styles */
        body, html {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: Arial, sans-serif;
            height: 100%;
        }

        .app-container {
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            height: 95vh;
        }

        /* Header styles */
        .app-header {
            background-color: #007bff;
            padding: 5px 10px;
            color: white;
            font-size: 0.5rem;
            font-weight: bold;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
            width: 100%;
            text-align: left;
        }

        /* Chat container */
        .chat-container {
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            height: 90%;
            padding: 20px;
            max-width: 600px;
            width: 100%;
            margin: 0 auto;
            border: 1px solid #ccc;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }

        /* Messages area */
        .messages {
            flex-grow: 1;
            margin: 0 auto;
            max-width: 600px;
            width: 100%;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            align-items: stretch;
        }

        /* Individual message styling */
        .message {
            padding: 10px;
            margin-bottom: 10px;
            border-radius: 5px;
            max-width: 300px;
            word-wrap: break-word;
            box-sizing: border-box;
        }

        /* Message alignment for other users */
        .message.other-user {
            background-color: #f1f1f1;
            align-self: flex-start;
        }

        /* Message alignment for user */
        .message.user {
            background-color: #007bff;
            color: white;
            align-self: flex-end;
        }

        /* Input area */
        .input-area {
            display: flex;
            width: 100%;
        }

        input {
            flex-grow: 1;
            padding: 10px;
            font-size: 1rem;
            border: 1px solid #ccc;
            border-radius: 4px;
            margin-right: 10px;
        }

        button {
            padding: 10px 20px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }

        button:hover {
            background-color: #0056b3;
        }

        /* Responsive adjustments */
        @media (max-width: 768px) {
            .chat-container {
                max-width: 100%;
                padding: 10px;
            }

            button {
                padding: 10px;
            }

            input {
                font-size: 0.9rem;
            }
        }

        @media (max-width: 480px) {
            .input-area {
                flex-direction: column;
            }

            input {
                width: 100%;
                margin-bottom: 10px;
            }

            button {
                width: 100%;
            }
        }
    </style>
</head>
<body>
    <div class="app-container">
        <!-- Header -->
        <header class="app-header">
            <h1>Anonymous Chat</h1>
        </header>

        <!-- Chat container -->
        <div class="chat-container">
            <div class="messages" id="messages">
                <!-- Messages will be added here -->
            </div>

            <!-- Input area -->
            <div class="input-area">
                <input type="text" id="messageInput" placeholder="Type a message...">
                <button onclick="sendMessage()">Send</button>
            </div>
        </div>
    </div>

    <script>
        const messagesContainer = document.getElementById('messages');
        const messageInput = document.getElementById('messageInput');

        function addMessage(msg) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${msg.sender === 'Me' ? 'user' : 'other-user'}`;
            messageDiv.innerHTML = `<strong>${msg.sender}:</strong> ${msg.message}`;
            messagesContainer.appendChild(messageDiv);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }

        function sendMessage() {
            const inputValue = messageInput.value.trim();
            if (inputValue) {
                const userMessage = { sender: 'Me', message: inputValue };
                addMessage(userMessage);
                messageInput.value = '';
                socket.send(inputValue);
            }
        }

        // Initialize WebSocket connection
        const socket = new WebSocket(`ws://${window.location.host}/room/websocket`);

        socket.onmessage = (event) => {
            const data = event.data;

            if (data.startsWith('User ') && data.includes('joined the chat')) {
                const newMessage = { sender: event.data.split(' joined')[0], message: ' joined the chat' };
                addMessage(newMessage);
            } else {
                const newMessage = { sender: event.data.split(':')[0], message: event.data.split(':')[1] };
                addMessage(newMessage);
            }
        };
    
    </script>
</body>
</html>
"""

@app.get("/")
async def get():
    return HTMLResponse(html)
