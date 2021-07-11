import asyncio
from bleak import BleakClient

address = "18:04:ed:62:5b:ac"
MODEL_NBR_UUID = "02a65821-0003-1000-2000-b05cb05cb05c"

async def run(address):
    async with BleakClient(address) as client:
        model_number = await client.read_gatt_char(MODEL_NBR_UUID)
        print("Model Number: {0}".format("".join(map(chr, model_number))))

loop = asyncio.get_event_loop()
loop.run_until_complete(run(address))