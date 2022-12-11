import sys, socket, threading, time
HOST = (("0.0.0.0", 80))
MTU = 4096
EdgeSession = []
c = s = t = None
def reset_session(timeout):
    global EdgeSession
    while True:
        time.sleep(timeout)
        EdgeSession = []
def reset_thread(timeout):
    global t
    t = threading.Thread(target = reset_session, args = (timeout,))
    t.start()
def data_template(sessions_dict):
    BODY = "<div>"
    for session in sessions_dict:
        BODY += "<a href=\"" + session["url"] + "\">" + session["name"] + "</a></br>\n"
    BODY += "</div>"
    SCRIPT =\
"""
window.onload = function()
{
    setInterval(function()
    {
        xmlhttp = new XMLHttpRequest();
        xmlhttp.open("RSVP", "Google", true);
        xmlhttp.onreadystatechange = function()
        {
            if ((xmlhttp.readyState == 4) && (xmlhttp.status == 200))
            {
                location.reload();
            }
        }
        xmlhttp.send("https://www.google.co.uk:443")
    }, 3000);
}
""".removeprefix("\n").removesuffix("\n")
    STYLE = \
"""
* { background: black; font-family: sans-serif; font-size: 20pt; }
""".removeprefix("\n").removesuffix("\n")
    DATA = \
"""
<title>RSVP</title>
<script>{}</script>
<style>{}</style>
{}
""".removeprefix("\n").removesuffix("\n").format(SCRIPT, STYLE, BODY)
    RSVP = \
"""
HTTP/1.1 200 OK
Content-Length: {}
Content-Type: text/html
Access-Control-Allow-Origin: *

{}
""".removeprefix("\n").removesuffix("\n").format(len(DATA), DATA)
    return RSVP.encode()
def reconnect():
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(HOST)
    s.listen(10)
def main():
    global EdgeSession, c, s, t
    print("[RSVP]: Starting Server")
    reset_thread(60)
    reconnect()
    while True:
        try:
            c, d = s.accept()
            msg, conn = c.recvfrom(MTU)
            if (msg[0:4] == b"RSVP"):
                if (msg[5:6] == b"/"):
                    data = msg.decode().replace("\r\n", "\n")[6:]
                    name = data.split("\n")[0].removesuffix(" HTTP/1.1")
                    url = data.rsplit("\n\n")[-1]
                    EdgeSession.append({"name": name, "url": url})
                    c.sendto(b"HTTP/1.1 200 OK", d)
            elif (msg[0:3] == b"GET"):
                if (msg[3:6] == b" / "):
                    RSVP = data_template(EdgeSession)
                    c.sendto(RSVP, d)
                else:
                    c.sendto(b"HTTP/1.1 200 OK", d)
            c.close()
        except Exception as error:
            print(error, file = sys.stderr)
            try:
                if c != None:
                    c.close()
            except:
                pass
            reconnect()
    s.close()
if __name__ == "__main__":
    main()
