
# Webhook Event Handling and Real-Time Notification Approaches

Documentation for Django based websocket app. 

The task is to handle webhook events sent from Mandrill and notify user interfaces in real-time. There are several ways to achieve this, including:

- Server-Sent Events (SSE)
- WebSocket Connections
- Message Queues with Long Polling

# Server-Sent Events (SSE) (Alternative Method)

How it works:

- The server keeps an HTTP connection open and streams new events to the client as they occur.

- Example: The server sends new Mandrill events in real-time over the same open connection.

Advantages:

- Low latency: Updates are sent immediately.

- Simple implementation: SSE is easier to manage compared to WebSockets.

- Native browser support: SSE works out of the box with modern browsers using the `EventSource` API.

Disadvantages:

- Unidirectional communication: Only the server can send messages; the client cannot send data back over the same connection.

- Connection limits: Browsers limit the number of simultaneous SSE connections.

- Compatibility issues: Not supported in older browsers or environments that block long-running HTTP connections.

Conclusion: SSE is good for simple real-time updates, but it lacks bidirectional communication.

# WebSocket Connections (Ideal Solution)

How it works:

- WebSocket creates a persistent, bidirectional connection between the server and client.

- Example: When Mandrill events occur, the server pushes them to the client over the WebSocket connection.

Advantages:

- Low latency: Instant updates are pushed to the client/customer.

- Bidirectional communication: The client can also send data to the server if needed.

- Efficient: WebSockets minimize overhead since the connection stays open and doesn't require repeated handshakes like HTTP.

Disadvantages: 

- Complex setup: Requires additional infrastructure, like Redis for Django Channels.

- Connection limits: WebSocket servers need to manage concurrent connections efficiently.

- Firewall/Proxy restrictions: WebSockets may be blocked by strict network policies.

Conclusion: WebSockets provide the best balance of real-time performance and efficiency, making them ideal for this task where instant feedback is required.

# Why WebSockets Are Ideal

Real-Time Requirement:

- The goal is to notify users immediately when events (like `open` or `click`) are triggered in Mandrill.

- WebSockets offer the fastest way to push notifications without waiting for a polling interval.

- A polling interval is the amount of time between consecutive polling requests from a client to a server. In polling, the client periodically sends HTTP requests to the server to check for new data or updates.

Bidirectional Communication:

- Even though I am not tasked to send messages back to the server, WebSockets support future extensibility if needed.

Efficient Use of Resources:

- WebSockets maintain a single open connection, reducing network overhead compared to repeated HTTP requests. Specfically using Redis and Django Channels.

Highly Scalable with Django Channels:

- While using Django and surfing through documentation and looking up resources I found that Django is super useful when needing to scale up a application in the future.

- Redis ensures scalability and message persistence even in distributed environments.

# How Django and Redis Work Together

Django Channels: WebSockets and Real-Time Support:

- Django Channels extends Django’s native HTTP handling to support WebSockets, long-lived connections, and asynchronous processing.

- When Mandrill sends webhook events, Django Channels can process them asynchronously and notify clients through WebSockets.

Why Django Channels?

- It supports persistent WebSocket connections.

- It can handle multiple connections simultaneously.

- It uses asynchronous consumers, which are more efficient than traditional synchronous views.

Redis as a Message Broker:

- Redis acts as a channel layer for Django Channels, meaning it manages the messages between webhook events and WebSocket clients.

- Redis ensures that messages are sent reliably and efficiently, even if the server is handling many users at once.

How Redis Helps:

- Real-Time Delivery: Messages are stored temporarily in Redis and delivered to WebSocket clients instantly.

# Conclusion 

WebSockets provide the best balance of real-time communication, efficiency, and scalability, making them the ideal solution for this task.
## How to Get a Successful Webhook

#### Step 1: Run Redis Server

```bash
redis-server
```

#### Step 2: Run Django Server in a Separate Terminal

```bash
python manage.py runserver
```

#### Step 3: Run Ngrok in a Third Terminal

```bash
ngrok http 8000
```

Note: You may need to update the ALLOWED_HOSTS setting in your Django project to include the Ngrok URL provided `(e.g., https://<your-ngrok-url>.ngrok-free.app).`

#### Step 4: Send a cURL Request from Another Terminal

Open the `curl.txt` file in your project directory.

Copy and paste the following cURL command into your terminal to test the webhook:
```bash
curl -X POST https://a8d2-207-162-137-211.ngrok-free.app/mandrill/ \
-H "Content-Type: application/json" \
-d '[
      {
        "event": "open",
        "msg": { "_id": "12345", "email": "test@example.com" },
        "ts": 1635098273
      },
      {
        "event": "click",
        "msg": { "_id": "67890", "email": "user@example.com" },
        "ts": 1635098373
      }
    ]'
```

#### Optional: Monitor Requests with Ngrok’s Web Interface
You can also view the details of your cURL request by visiting Ngrok’s local web interface:
```bash
http://127.0.0.1:4040
```