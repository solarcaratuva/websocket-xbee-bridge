#!/usr/bin/env python

import asyncio
import json
import sys
import time
import websockets

from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice  
from digi.xbee.models.address import XBee64BitAddress

WS_URI = "ws://localhost:8080/ws"
XBEE_ADDRESS = "0013A20041C4ACC3"
CAN_IDS = [0x106, 0x115, 0x123, 0x180, 0x181, 0x201, 0x280, 0x281, 0x301, 0x315, 0x325, 0x332, 0x406, 0x416, 0x426, 0x434, 0x444, 0x454, 0x464, 0x480, 0x481]

async def main():
    args = sys.argv[1:]
    
    PORT = args[0]
    BAUD_RATE = args[1]

    xbee = XBeeDevice(PORT, BAUD_RATE)
    xbee.open()

    remote = RemoteXBeeDevice(xbee, XBee64BitAddress.from_hex_string(XBEE_ADDRESS))

    async with websockets.connect(WS_URI) as ws:
        subscribe_command = {"subscribe": CAN_IDS};
        await ws.send(json.dumps(subscribe_command))
        print("sent subscribe command")

        while True:
            data = await ws.recv()
            xbee.send_data(remote, data)
            print(data)

asyncio.run(main())
