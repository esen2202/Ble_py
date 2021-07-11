import sys
import asyncio
import platform

from bleak import BleakClient

ADDRESS = "18:04:ed:62:5b:ac"
     
if len(sys.argv) == 2:
    ADDRESS = sys.argv[1]


async def print_services(mac_addr: str):
    async with BleakClient(mac_addr) as client:
        svcs = await client.get_services()
        print("Services:")
        for service in svcs:
            print(service)


loop = asyncio.get_event_loop()
loop.run_until_complete(print_services(ADDRESS))
