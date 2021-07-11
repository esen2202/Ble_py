
from bleak import BleakClient
import asyncio

address1 = "D8:A0:1D:55:EE:8A"
UUID1 = "beb5483e-36e1-4688-b7f5-ea07361b26a8"

address2 = "94:B9:7E:93:21:76"
UUID2 = "beb5483e-36e1-4688-b7f5-ea07361b26a2"

adresses = [address1, address2] 
UUIDs = [UUID1, UUID2]

def run(addresses, UUIDs):
    loop = asyncio.get_event_loop()
    task = asyncio.gather(*(connect_to_device(address, UUID) for address, UUID in zip(addresses, UUIDs)))
    loop.run_until_complete(task)

async def connect_to_device(address, UUID):
    print("starting", address, "loop")
    async with BleakClient(address, timeout=5.0) as client:
        print("connected to", address)
        tasks = {client.read_gatt_char(UUID)}
        while(True):
            done, not_done = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
            for tasks in done:
                try:
                    print(await tasks)
                except Exception as e:
                    print(e)
                not_done.add(tasks)
            tasks = not_done

if __name__ == "__main__":
    run(adresses, UUIDs)