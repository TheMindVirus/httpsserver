import sys, socket, threading, time, json

### RSVP Server - HTTP TCP Bonjour mDNS v0.0.0.0.0.0.0.0.0.
### RINSE Protocol - RINSE IS NOT SDP EDGE
### TODO: Add REST Support

HOST = (("0.0.0.0", 80))
MTU = 4096 # 1500

EdgeSession = [{"name": "Google", "url": "https://www.google.com:443"},]
EdgeSignal = None

ERROR_TIMEOUT = type(TimeoutError())
TYPE_LIST = type(list())
    
def reset_session(timeout):
    global EdgeSession
    while True:
        time.sleep(timeout)
        EdgeSession = [{"name": "Google", "url": "https://www.google.com:443"},]
        reconnect()

def reset_thread(timeout):
    global t
    t = threading.Thread(target = reset_session, args = (timeout,))
    t.start()

def data_template(sessions):
    DATA = json.dumps(sessions, indent = 4)
    if (type(sessions) == TYPE_LIST):
        DATA = DATA.removeprefix("[").removesuffix("]")
        DATA = "{" + DATA + "}" # Surely there is a better way of doing this?
    RSVP = \
"""
HTTP/1.1 200 OK
Content-Length: {}
Content-Type: application/json
Access-Control-Allow-Origin: *

{}
""".removeprefix("\n").removesuffix("\n").format(len(DATA), DATA)
    return RSVP.encode()

def reconnect():
    global EdgeSignal
    EdgeSignal = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    EdgeSignal.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #EdgeSignal.setsockopt(socket.SOL_SOCKET, socket.SO_SNDTIMEO, 1000) # Blank Message
    #EdgeSignal.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, 1000) # Blank Message
    EdgeSignal.bind(HOST)
    EdgeSignal.listen(socket.SOMAXCONN)
    return EdgeSignal

def service_thread(c, d):
    global EdgeSession, EdgeSignal
    try:
        print(c, d)
        c.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #c.setsockopt(socket.SOL_SOCKET, socket.SO_SNDTIMEO, 1000) # Blank Message
        c.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, 1000) # Blank Message
        msg, conn = c.recvfrom(MTU)
        if (msg[0:4] == b"RSVP"):
            if (msg[5:6] == b"/"): # Not a specified requirement
                data = msg.decode().replace("\r\n", "\n")[6:]
                name = data.split("\n")[0].removesuffix(" HTTP/1.1")
                url = data.rsplit("\n\n")[-1]
                #url, conn2 = c.recvfrom(MTU) # Await Blocking Call.
                print(name)
                print(url)
                #if not app_name or not url: #nor?
                #    c.sendto(b"HTTP/1.1 400 Bad Request", d)
                #    raise Exception("Error 400 Bad Request")
                EdgeSession.append({"name": name, "url": url})
                c.sendto(b"HTTP/1.1 200 OK", d)
        elif (msg[0:3] == b"GET"):
            if (msg[3:6] == b" / "):
                RSVP = data_template(EdgeSession)
                print(RSVP)
                print(d)
                c.sendto(RSVP, d)
                c.sendto(b"HTTP/1.1 200 OK", d)
        c.close()
    except Exception as error:
        try:
            if c != None:
                c.close()
        except:
            pass
        if (type(error) == ERROR_TIMEOUT):
            print("Timed Out")
        else:
            print(error, file = sys.stderr)

def main():
    global EdgeSession, EdgeSignal
    c = None
    d = None
    a = None
    t = None
    cc = []
    gg = []
    print("[RSVP]: Starting Server")
    reset_thread(60)
    reconnect()
    while True:
        try:
            c, d = EdgeSignal.accept()
            a = threading.Thread(target = service_thread, args = (c, d))
            a.start()
            cc.append(a)
            gg = []
            for i in range(0, len(cc)):
                try:
                    if not cc[i].is_alive():
                        gg.append(i)
                except:
                    gg.append(i)
            for i in gg:
                cc.pop(i)
        except Exception as error:
            print(error, file = sys.stderr)
    EdgeSignal.close()

if __name__ == "__main__":
    main()




# This script was made longer and more complicated to understand
# because of the penetrative actions of security professionals.
# Their only end goal is to make it so obfuscated that it no longer makes sense.




# The obfuscation to the extent required to stop penetration tests
# will only result in further complications to the services that the script provides.
# For example, a Blank TCP message will completely halt the server until restart.




# Requiring a watchdog timer to reset the service makes it somewhat
# less efficient than when it was just a service definition script.
# This is especially the case when there is no watchdog or when it fails.




# Dual or Triple Redundancy is required to keep services running.
# When one client halts the server connection, it should not affect other clients.
# Therefore, threading has been made compulsory for this isolation whether it is liked or not.




# Fixed-function hardware will operate at high speed but also high unreliability.
# Software-only solutions will operate either slowly and reliably or quickly and fail-fast.
# Reconfigurable hardware will operate at high speed whilst maintaining reliability in parallel.




# The speed of the service is also bound by the laws of physics
# that apply to the machine running the service. Thermals and Electromagnatism
# are key factors requiring more heavy maintenance, Virtual Machines more so.




# Asynchronous code never required an entire rewrite of any project.
# Instead, async is being required to be added to every function
# and await is beign required to be added to every function call.




# The idea that a blocking call is made worse by having to await it indefinitly
# and requires a keyword has made it more inefficient, especially for porting
# to another language without such keywords. This just becomes synchronous.




# Not only is asynchronous code not done immediately when specified,
# it is then delayed and causes further coherency complications.
# A series of pipelined Events is ideal without .then().then().then() and async/await.




# Decorators with the @ symbol have been added to several interpreted languages
# including Python and Java. This has made code less comprehendable and more
# chaotic, where whole classes are written and then completely overriden.




# LINE 200
