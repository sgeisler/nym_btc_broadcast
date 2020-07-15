#!/bin/python3

import asyncio
import json
import websockets
import requests

ws = None
uri = "ws://127.0.0.1:1978"
blockstream_api = "https://blockstream.info/testnet/api/tx"

async def connect():
    global ws
    if not ws:
        ws = await websockets.connect(uri)
    return ws

async def get_self_id():
    ws = await connect()
    await ws.send('{"type": "selfAddress"}')
    self_address = json.loads(await ws.recv())
    return self_address["address"]

async def receive_msg():
    ws = await connect()
    msg = await ws.recv()
    return msg


async def main():
    me = await get_self_id()
    print("Listening on {}".format(me))

    while True:
        msg = await receive_msg()
        try:
            r = requests.post(blockstream_api, data=msg)
            print("Broadcasted transaction {}".format(r.text))
        except requests.exceptions.RequestException as e:
            print("There was an error: {}".format(e))

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
