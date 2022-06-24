#python.exe -m pip install websockets
import websockets, asyncio, threading

class websockettest:
    def __init__(self):
        self.server = threading.Thread(target = self.server_main)
        self.client = threading.Thread(target = self.client_main)
        self.server.start()
        self.client.start()

    def server_main(self):
        asyncio.run(self.serve("localhost", 8765))

    def client_main(self):
        asyncio.run(self.connect("localhost", 8765))

    async def serve(self, host, port):
        async with websockets.serve(self.acknowledge, host, port):
            await asyncio.Future()

    async def acknowledge(self, websocket):
        async for message in websocket:
            await websocket.send("[ACK]")

    async def connect(self, host, port):
        uri = "ws://" + str(host) + ":" + str(port)
        async with websockets.connect(uri) as websocket:
            while True:
                try:
                    await websocket.send("[TEST]")
                    data = await websocket.recv()
                    print(data)
                except Exception as error:
                    print(error)

if __name__ == "__main__":
    websockettest()
    while True:
        pass
