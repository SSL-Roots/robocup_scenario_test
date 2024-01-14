
import socket


class RefereeSender:
    def __init__(self, addr, port):
        self._addr = addr
        self._port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Configure multicast TTL
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)

    def send(self, msg: bytes):
        try:
            self.sock.sendto(msg, (self._addr, self._port))
        except Exception as e:
            print("Failed to send referee message. Details: {}".format(e))
