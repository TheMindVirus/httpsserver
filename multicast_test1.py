import socket, struct, codecs, time

multicast_address = "224.0.1.2" # "211.1.1.1"
localhost_address = "0.0.0.0" # 127.0.0.254

port = 12345
mtu = 1500

multicast = int.from_bytes(socket.inet_aton(multicast_address), "little")
localhost = int.from_bytes(socket.inet_aton(localhost_address), "little")
mreq = struct.pack("LL", multicast, localhost)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, 0)
s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)
s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
s.bind((localhost_address, port))

running = True
while running:
    s.sendto(b"Message", ((multicast_address, port)))
    data = s.recvfrom(mtu)
    print(data)
    time.sleep(1)
