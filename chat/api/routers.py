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
            max-width: 350px;
            word-wrap: break-word;
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
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

        .message .timestamp {
            font-size: 0.8rem;
            color: #1a1919;
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

        function formatTimestamp(date) {
            const hours = String(date.getHours()).padStart(2, '0');
            const minutes = String(date.getMinutes()).padStart(2, '0');
            return `${date.toISOString().split('T')[0]} ${hours}:${minutes}`;
        }

        function addMessage(author, message, timestamp) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${author === 'Me' ? 'user' : 'other-user'}`;
            messageDiv.innerHTML = `<span class="timestamp">${timestamp}</span><strong>${author}:</strong> ${message}`;
            messagesContainer.appendChild(messageDiv);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }

        function sendMessage() {
            const inputValue = messageInput.value.trim();
            if (inputValue) {
                const timestamp = formatTimestamp(new Date());
                addMessage('Me', inputValue, timestamp);
                messageInput.value = '';
                socket.send(inputValue);
            }
        }

        const socket = new WebSocket(`ws://${window.location.host}/room/websocket`);

        socket.onmessage = (event) => {
            const data = event.data;
            const timestamp = formatTimestamp(new Date());

            if (data.startsWith('User ') && data.includes('joined the chat')) {
                addMessage(data.split(' joined the chat')[0], 'joined the chat', timestamp);
            } else {
                const [author, ...messageParts] = data.split(':');
                const message = messageParts.join(':').trim(); // Join the rest of the message content back together
                addMessage(author.trim(), message, timestamp);
            }
        };

    </script>
</body>
</html>

"""

@app.get("/")
async def get():
    return HTMLResponse(html)
