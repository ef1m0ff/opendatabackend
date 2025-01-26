from typing import List

import httpx
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from utils import STRAPI_BASE_URL

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

users_db = {}
websocket_connections: List[WebSocket] = []  # Store active WebSocket connections


class PostRequestModel(BaseModel):
    allowsWriteToPm: bool
    firstName: str
    id: int
    languageCode: str
    lastName: str
    photoUrl: str
    username: str

    event_id: int
    check: bool


class WebSocketModel(BaseModel):
    user_id: int
    fullname: str
    username: str




@app.post("/events/")
async def post_event(data: PostRequestModel):
    print(f"Received event with data: {data}")
    dataUser = None
    async with httpx.AsyncClient() as client:
        get_url = f"{STRAPI_BASE_URL}/tg-users?filters[tg_id][$eq]={data.id}&populate=*"
        response_get = await client.get(get_url)
        if response_get.status_code == 200:
            print(f"GET request to Strapi successful: {response_get.json()}")
            if not response_get.json()['data']:
                data_send = {"data": {
                    "username": data.username,
                    "tg_id": str(data.id),
                    "full_name": data.firstName + ((" " + data.lastName) if data.lastName else ''),
                    "avatar_url": data.photoUrl
                }}
                response_post = await client.post(f"{STRAPI_BASE_URL}/tg-users", json=data_send)
                dataUser = response_post.json()['data']
        else:
            print(f"GET request failed: {response_get.status_code}")
        if not dataUser:
            dataUser = response_get.json()['data'][0]

        documentId = dataUser['documentId']

        if 'events' in dataUser:
            events = set(i['id'] for i in dataUser['events'])
        else:
            events = set()
        if data.check:
            events.add(data.event_id)
        elif data.event_id in events:
            events.remove(data.event_id)

        response_put = await client.put(
            f"{STRAPI_BASE_URL}/tg-users/{documentId}",
            json={"data": {"events": list(events)}}
        )
        if response_put.status_code == 200:
            print(f"PUT request to Strapi successful: {response_put.json()}")
        else:
            print(f"PUT request failed: {response_put.status_code}")

    return {"status": "success", "events": list(events), "documentId": documentId}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, user: WebSocketModel):
    await websocket.accept()
    users_db[user.user_id] = {"fullname": user.fullname, "username": user.username}
    websocket_connections.append(websocket)

    await broadcast_user_update()

    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received message from user {user.user_id}: {data}")
            await broadcast_user_update()
    except WebSocketDisconnect:
        users_db.pop(user.user_id, None)
        websocket_connections.remove(websocket)
        await broadcast_user_update()


async def broadcast_user_update():
    message = {"users": list(users_db.values())}
    for connection in websocket_connections:
        await connection.send_json(message)


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8020, ws='websockets')
