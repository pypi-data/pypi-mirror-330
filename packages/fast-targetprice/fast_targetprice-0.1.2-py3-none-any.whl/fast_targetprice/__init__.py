import json
import os
import threading
import asyncio
import websockets
import struct

class SITE():
    buff163 = 0
    youpin898 = 1

class WebSocketClient:
    def __init__(self, server_url, api_key):
        self.server_url = server_url
        self.api_key = api_key
        self.ws = None
        self.loop = None
        self.thread = None
        self.lock = threading.Lock()
        self._start_loop()

    def _start_loop(self):
        """Tạo một event loop chạy trong thread riêng."""
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()

    def _run_loop(self):
        """Chạy asyncio event loop trong thread riêng."""
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def _run_coroutine(self, coroutine):
        """Chạy coroutine trong event loop của thread."""
        return asyncio.run_coroutine_threadsafe(coroutine, self.loop).result()

    def connect(self):
        """Hàm đồng bộ để kết nối đến WebSocket."""
        with self.lock:
            return self._run_coroutine(self._async_connect())

    async def _async_connect(self):
        """Hàm async để kết nối WebSocket và xác thực API key."""
        if self.ws is None or self.ws.close_code is not None: 
            self.ws = await websockets.connect(self.server_url)
            api_key_bytes = bytes.fromhex(self.api_key)
            await self.ws.send(api_key_bytes)
            try:
                byte_value = await asyncio.wait_for(self.ws.recv(), timeout=2)
                response = int.from_bytes(byte_value, "big")
                if response == 0:
                    print("Authenticated successfully.")
                elif response == 1:
                    print("Unauthorized API key, closing connection.")
                elif response == 2:
                    print(f"API Key {self.api_key} is already in use, closing connection.")
            except asyncio.TimeoutError:
                print("Authentication failed or timed out.")
                await self.ws.close()
                raise ConnectionError("Authentication failed.")

    def get_price(self, site_id:SITE, item_id):
        """Hàm đồng bộ lấy giá trị từ server, có thể gọi từ nhiều thread."""
        with self.lock: 
            return self._run_coroutine(self._async_get_price(site_id, item_id))

    async def _async_get_price(self, site_id, item_id):
        """Hàm async để gửi yêu cầu và nhận giá trị từ server."""
        try:
            if self.ws is None or self.ws.close_code is not None: 
                await self._async_connect()
            message = struct.pack("<BH", site_id, item_id)
            await self.ws.send(message)
            response = await asyncio.wait_for(self.ws.recv(), timeout=2)
            if len(response) == 15:
                received_site_id, received_item_id, price1, price2, price3 = struct.unpack("<BHIII", response)
                return price1, price2, price3
            else:
                print("Invalid response length:", len(response))
                return None
        except asyncio.TimeoutError:
            print("No response from server.")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None

    def close(self):
        """Đóng kết nối WebSocket."""
        with self.lock: 
            self._run_coroutine(self._async_close())

    async def _async_close(self):
        """Hàm async để đóng WebSocket."""
        if self.ws and not self.ws.close_code:
            await self.ws.close()
            await self.ws.wait_closed()
            print("WebSocket connection closed.")
        self.loop.stop()

class CONVERTER:
    def __init__(self):
        with open(os.path.join(os.path.dirname(__file__), "dataset.json"),"r",encoding="utf-8") as f:
            self.__dataset = json.load(f)

    def getId(self,itemName):
        if item := next((item for item in self.__dataset if item["CommodityHashName"] == itemName), None):
            return item["id"]
    
    def getItemName(self,id):
        if item:= next((item for item in self.__dataset if item["id"] == int(id)), None):
            return item["CommodityHashName"]
