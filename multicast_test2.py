import socket, struct, codecs, time, atexit

port = 12345
mtu = 1500

multicast = "224.0.1.2" # edge:// protocol handler?
localhost = "0.0.0.0" # localedge and .edge DNS names?

multicast_address = multicast
localhost_address = localhost

multicast_address = socket.inet_aton(multicast_address)
localhost_address = socket.inet_aton(localhost_address)

multicast_address = codecs.encode(multicast_address, "hex")
localhost_address = codecs.encode(localhost_address, "hex")

multicast_address = int(multicast_address, 16)
localhost_address = int(localhost_address, 16)

multicast_address = struct.pack(">L", multicast_address) # Endian to match iOS
localhost_address = struct.pack(">L", localhost_address) # May be opposite sign

#mreq = struct.pach("<L<L", multicast_address, localhost_address)
mreq = multicast_address + localhost_address
# For python2 socket only, this has changed

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_IP)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)
s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
s.bind((localhost, port))

running = True

def cleanup():
    global s, running
    running = False
    s.setsockopt(socket.IPPROTO_IP, socket.IP_DROP_MEMBERSHIP, mreq)
atexit.register(cleanup)

while running:
    s.sendto(b"Message", ((multicast, port)))
    data = s.recvfrom(mtu)
    print(data) # Only 1 message received out of 3, requires thread + onreceive
    time.sleep(1)
