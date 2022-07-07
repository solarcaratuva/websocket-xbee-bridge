#!/usr/bin/env python

import asyncio
import json
import sys
import time
import websockets

from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice  
from digi.xbee.models.address import XBee64BitAddress

async def main():
    args = sys.argv[1:]
    
    PORT = args[0]
    BAUD_RATE = args[1]

    xbee = XBeeDevice(PORT, BAUD_RATE)
    xbee.open()

    remote = RemoteXBeeDevice(xbee, XBee64BitAddress.from_hex_string("0013A20041C4ACC3"))

    uri = "ws://localhost:8080/ws"
    async with websockets.connect(uri) as websocket:
        subscribe_command = {"subscribe": [0x123, 0x201, 0x301, 0x315, 0x325, 0x406, 0x426]};
        await websocket.send(json.dumps(subscribe_command))
        print("sent subscribe command")

        while True:
            data = await websocket.recv()
            xbee.send_data(remote, data)
            print(data)

asyncio.run(main())
