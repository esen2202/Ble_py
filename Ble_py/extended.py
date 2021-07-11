import asyncio
from bleak import BleakClient
# I have omitted the not interesting code
async def __start(self, loop):
        self.lock = asyncio.Lock()
	async with BleakClient(self.mac) as client:
		self.client = client
		self.disconnected_event = asyncio.Event()

		def disconnect_callback(client):
			loop.call_soon_threadsafe(self.disconnected_event.set)

		client.set_disconnected_callback(disconnect_callback)
		is_connected = await client.is_connected()
		self.connected_event.set()
		self.start_tpt_time = time.time()
		await client.start_notify(NOTIFY_CHAR_UUID, self.data_notification_handler)
		while True:
			try:
				if self.disconnected_event.is_set():
					await self.on_disconnect(client)
					return
				if self.__was_closed and self.__target_ble_queue.empty():
					self.log.info("BLE closing {}", self.mac)
					return
				data_packet = self.__target_ble_queue.get_nowait()
				###########
				total_length = len(data_packet.data)
				bytes_sent = 0
				while bytes_sent < total_length:
					to_send = min(self.config.max_ble_packet_size_bytes - 8, total_length - bytes_sent)
					content = data_packet.data[bytes_sent: bytes_sent + to_send]
					padded_content = self.pad_packet(content)
					await client.write_gatt_char(WRITE_CHAR_UUID, padded_content)
					bytes_sent += to_send

				#############
				self.log.debug("write whole non padded packet {} with {} bytes via BLE done", data_packet.id, total_length)
			except Empty:
				await asyncio.sleep(0.5)
				if not await client.is_connected():
					error_message = "substrate {0} not connected".format(self.mac)
					self.log.error(error_message)
					raise Exception(error_message)

def data_notification_handler(self, sender, data):
    try:
        self.lock.acquire()
        data_packet = DataPacket(bytearray(data[4:-4]))
        self.__calculate_tpt(data)
        self.__check_crc(data)
        self.__check_index(data)
        self.__target_tcp_queue.put_nowait(data_packet)
    except Full:
        first_msg = self.__target_tcp_queue.get()
        self.__target_tcp_queue.put(DataPacket(bytearray(data[4:-4])))
    except Exception as e:
        import traceback
        self.log.fatal("BLE data handler Exception :\n" + str(e) + str(traceback.format_exc()))
    finally:
        self.lock.release()
		
def __check_index(self, data: bytearray):
    data_len = len(data)
    if data_len > 8:
        recv_index = struct.unpack_from("<I", data, 0)[0]
        #self.log.fatal("index error computed = {}",recv_index)
        if self.receive_index == -1:
            self.receive_index = recv_index
        else:
            self.receive_index += 1
            if self.receive_index != recv_index:
                self.log.fatal("index error computed = {} actual = {}", self.receive_index, recv_index)
                self.log.fatal("content of index error BLE packet \n{}\nlength {}", list(data), data_len)
                self.receive_index = recv_index  # align counter, wait for next failure
                #raise Exception("wrong index")
    else:
        self.log.fatal("data packet size is {} less than 9.", data_len)
        self.log.fatal("content short BLE packet \n{}\nlength {}", list(data), data_len)
        raise Exception("data too short")
