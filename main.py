import os

import httpx
from dotenv import load_dotenv
from telethon import TelegramClient, events

from utils import model_ask, STRAPI_BASE_URL, find_datetime

load_dotenv()

api_id, api_hash = int(os.getenv("API_ID")), os.getenv("API_HASH")
phone = os.getenv("PHONE")
client = TelegramClient(phone, api_id, api_hash)


@client.on(events.NewMessage(outgoing=False))
async def my_event_handler(event: events.newmessage.NewMessage.Event):
    res = model_ask(event.raw_text)
    data_dict = {}

    for line in res.strip().split("\n"):
        if ": " in line:
            key, value = line.split(": ", 1)
            data_dict[key.strip()] = value.strip()
    dt = data_dict['Date and Time'] if 'Date and Time' in data_dict else data_dict[
        'Date'] if 'Date' in data_dict else None
    if not dt:
        print('No date in message', data_dict)
        return
    maybe_dt = find_datetime(dt)
    if not maybe_dt:
        print('No date in dt', dt, data_dict)
        return

    frm = 'OFFLINE' if 'Format' not in data_dict else data_dict['Format'].upper()

    data_send = {"data": {
        "title": data_dict['Summary'] if 'Summary' in data_dict else event.raw_text.split('\n')[0],
        "start_date": maybe_dt.isoformat(),
        "short_description": data_dict['Summary'] if 'Summary' in data_dict else event.raw_text.split('\n')[0],
        "description": event.raw_text,
        "format": frm if frm in ['OFFLINE', 'ONLINE'] else 'OFFLINE',
        "location": data_dict['Location'] if 'Location' in data_dict else '-',
        "source_link": "https://t.me",
    }}
    async with httpx.AsyncClient() as cl:
        response_post = await cl.post(f"{STRAPI_BASE_URL}/events", json=data_send)
    print(data_dict)
    print(response_post)
    print(response_post.json())


if __name__ == '__main__':
    client.start()
    print('started')
    client.run_until_disconnected()
