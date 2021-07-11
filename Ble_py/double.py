import asyncio
from typing import Set

from bleak import BleakScanner, BleakClient
from bleak.backends.scanner import BLEDevice, AdvertisementData

PYBRICKS_SERVICE_UUID = "C5F50001-8280-46DA-89F4-6D8051E4AEEF"
PYBRICKS_CHAR_UUID = "C5F50002-8280-46DA-89F4-6D8051E4AEEF"


async def monitor(device: BLEDevice) -> None:
    """
    Monitors notifications from a BLE device until it disconnects.
    """
    disconnect_event = asyncio.Event()

    def handle_disconnect(client: BleakClient) -> None:
        print(f"disconnected from {client.address}")
        disconnect_event.set()

    def handle_notification(handle: int, value: bytearray) -> None:
        print(f"received {value} from {device.address}")

    async with BleakClient(device, disconnected_callback=handle_disconnect) as client:
        print(f"connected to {client.address}")
        await client.start_notify(PYBRICKS_CHAR_UUID, handle_notification)
        await disconnect_event.wait()


async def scan() -> None:
    """
    Scans for devices for 10 seconds and initiates a ``monitor`` for each
    discovered device.
    """

    # keep track of detected devices to avoid creating duplicate connections
    detected: Set[str] = set()

    def handle_detection(device: BLEDevice, adv: AdvertisementData) -> None:
        if PYBRICKS_SERVICE_UUID.lower() not in adv.service_uuids:
            return

        if device.address not in detected:
            detected.add(device.address)
            asyncio.create_task(monitor(device))

    async with BleakScanner(detection_callback=handle_detection):
        print("scanning...")
        await asyncio.sleep(10)
        print("done scanning.")


async def test() -> None:
    asyncio.create_task(scan())
    # wait forever
    await asyncio.Event().wait()


asyncio.run(test())

