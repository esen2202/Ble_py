import asyncio
from ctypes import *
from bleak import BleakClient

address = "18:04:ed:62:5b:ac"
MODEL_NBR_UUID = "02a65821-0003-1000-2000-b05cb05cb05c"

async def run(address):
    async with BleakClient(address) as client:
        #info = "{\"response_code\": 0,\"result\":12345}" # put short data here
        info = "{\"response_code\": 0,\"result\":\" This is a larger amount of data that I want to send: In a village of La Mancha, the name of which I have no desire to call to mind, there lived not long since one of those gentlemen that keep a lance in the lance-rack, an old buckler, a lean hack, and a greyhound for coursing. An olla of rather more beef than mutton, a salad on most nights, scraps on Saturdays, lentils on Fridays, and a pigeon or so extra on Sundays, made away with three-quarters of his income. The rest of it went in a doublet of fine cloth and velvet breeches and shoes to match for holidays, while on week-days he made a brave figure in his best homespun. He had in his house a housekeeper past forty, a niece under twenty, and a lad for the field and market-place, who used to saddle the hack as well as handle the bill-hook. The age of this gentleman of ours was bordering on fifty; he was of a hardy habit, spare, gaunt-featured, a very early riser and a great sportsman. They will have it his surname was Quixada or Quesada (for here there is some difference of opinion among the authors who write on the subject), although from reasonable conjectures it seems plain that he was called Quexana. This, however, is of but little importance to our tale; it will be enough not to stray a hair's breadth from the truth in the telling of it.\"}" # put your large data here
        length = len(info)
        factory_info_bytes = create_string_buffer(info.encode('utf-8'), length)
        await client.write_gatt_char(MODEL_NBR_UUID, factory_info_bytes.raw)

loop = asyncio.get_event_loop()
loop.run_until_complete(run(address))