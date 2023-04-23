import socket, struct, threading, time, atexit

port = 12345
mtu = 1500

multicast_address = "224.0.1.2" #EDGE, NTP + 1
localhost_address = "0.0.0.0"

multicast = int.from_bytes(socket.inet_aton(multicast_address), "little")
localhost = int.from_bytes(socket.inet_aton(localhost_address), "little")
mreq = struct.pack("LL", multicast, localhost)

s = None
thread = None
running = True

def main():
    global s, running, thread
    atexit.register(cleanup)
    try:
        reconnect()
    except:
        pass
    thread = threading.Thread(target = worker)
    thread.start()
    while running:
        try:
            s.sendto(b"Message", ((multicast_address, port)))
            time.sleep(1)
        except Exception as error:
            print(error)
            time.sleep(1)
            reconnect()

def reconnect():
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, 0)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    s.bind((localhost_address, port))

def worker():
    global s, running
    while running:
        try:
            data = s.recvfrom(mtu)
            receive(*data)
        except Exception as error:
            pass

#Message received 3 times:
# - 1 from multicast loopback
# - 1 from machine local loopback
# - 1 from network router loopback
#No way of telling which interface is which

def receive(message, connection):
    print(message, connection)

def cleanup():
    global s, running, thread
    running = False
    if s != None:
        thread.join()
        s.setsockopt(socket.IPPROTO_IP, socket.IP_DROP_MEMBERSHIP, mreq)
        s.close()

if __name__ == "__main__":
    main();
