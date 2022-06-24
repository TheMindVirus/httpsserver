#python.exe -m pip install websockets
import websockets, asyncio, threading
import ssl, pathlib

# https://www.digitalocean.com/community/tutorials/openssl-essentials-working-with-ssl-certificates-private-keys-and-csrs
# sudo openssl req -newkey rsa:2048 -nodes -keyout domain.key -x509 -days 365 -out domain.crt

### !!! USE HTTPSSERVER AND BROWSE TO https://localhost/websocketsecuretest.html !!! ###

class websockettest:
    def __init__(self):
        self.sssl = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        self.cssl = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        self.sssl.load_cert_chain("domain.crt", "domain.key")
        self.cssl.check_hostname = False #Fixed Hostname is an Absurd Assumption for Code
        #self.cssl.verify_mode = ssl.CERT_NONE
        self.cssl.load_verify_locations("domain.crt", "domain.key")
        self.server = threading.Thread(target = self.server_main)
        self.client = threading.Thread(target = self.client_main)
        self.server.start()
        #self.client.start()

    def server_main(self):
        asyncio.run(self.serve("localhost", 8769))

    def client_main(self):
        asyncio.run(self.connect("localhost", 8769))

    async def serve(self, host, port):
        async with websockets.serve(self.acknowledge, host, port, ssl = self.sssl):
            await asyncio.Future()

    async def acknowledge(self, websocket):
        async for message in websocket:
            await websocket.send("[ACK]")

    async def connect(self, host, port):
        uri = "wss://" + str(host) + ":" + str(port)
        async with websockets.connect(uri, ssl = self.cssl) as websocket:
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
