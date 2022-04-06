#!/usr/bin/python3
import socket, ssl, http.server
from PIL import Image

# https://www.digitalocean.com/community/tutorials/openssl-essentials-working-with-ssl-certificates-private-keys-and-csrs
# sudo openssl req -newkey rsa:2048 -nodes -keyout domain.key -x509 -days 365 -out domain.crt

CANVAS_FILE = "./web/canvas.png"

def update_image(x, y, c):
    x = int(x)
    y = int(y)
    c = int("0x" + str(c[1:]), 16)
    r, g, b = [(c >> 16) & 0xFF, (c >> 8) & 0xFF, c & 0xFF]
    img = Image.open(CANVAS_FILE)
    img.putpixel((x, y), (r, g, b))
    img.save(CANVAS_FILE)

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory = "web", **kwargs)

    def do_POST(self):
        length = int(self.headers["Content-Length"])
        data = self.rfile.read(length).decode("utf-8")
        cmds = data.split("x")
        if (len(cmds) == 3):
            self.send_response(200)
            self.wfile.write(data.encode("utf-8"))
            print(cmds)
            update_image(*cmds)
        else:
            self.send_response(500)
            self.wfile.write("Bad Request")

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        http.server.SimpleHTTPRequestHandler.end_headers(self)

ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ctx.load_cert_chain("domain.crt", "domain.key")
ctx.check_hostname = False
httpd = http.server.HTTPServer(("0.0.0.0", 443), Handler)
httpd.socket = ctx.wrap_socket(httpd.socket, server_hostname = "localhost")
httpd.serve_forever()

#update_image(*("500x500x#FF0000".split("x")))
