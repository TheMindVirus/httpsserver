import socket, ssl, http.server, subprocess

WEBROOT = "./web"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory = WEBROOT, **kwargs)

    def do_PY(self):
        program = str(self.path).encode()
        headers = b"[TEST OUTPUT OF " + program + b"]\r\n"
        message = b""
        # Optionally Communicate with MicroPython/CircuitPython Device
        command = "python " + str(WEBROOT) + program.decode()
        try:
            pipe = subprocess.run(command,
                shell = True, check = True, capture_output = True)
            message = pipe.stdout + pipe.stderr
        except Exception as error:
            message = str(error).encode()
        data = headers + message
        self.protocol_version = "HTTP/1.1"
        self.send_response(200, "OK")
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(data)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        http.server.SimpleHTTPRequestHandler.end_headers(self)

ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ctx.load_cert_chain("domain.crt", "domain.key")
ctx.check_hostname = False
httpd = http.server.HTTPServer(("0.0.0.0", 443), Handler)
httpd.socket = ctx.wrap_socket(httpd.socket, server_hostname = "localhost")
httpd.serve_forever()

