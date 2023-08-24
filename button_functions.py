import sys
import asyncio
import websockets
import json

async def authenticate(websocket, auth_token):
    auth_payload = {
        "type": "auth",
        "access_token": auth_token
    }
    await websocket.send(json.dumps(auth_payload))
    response = await websocket.recv()
    print(f"Authentication response: {response}")

# Function to send a command to the WebSocket server
async def send_command(websocket_url, auth_token, command):
    async with websockets.connect(websocket_url) as websocket:
        await authenticate(websocket, auth_token)
        await websocket.send(command)
        print(f"Sent command: {command}")
        response = await websocket.recv()
        print(f"Received response: {response}")

# Function to create a JSON service call
def call_light_service(service, entity_id):
    service_call = {
        "id": 24,
        "type": "call_service",
        "domain": "light",
        "service": service,
        "target": {
            "entity_id": entity_id
        }
    }
    service_call_json = json.dumps(service_call)
    return service_call_json
