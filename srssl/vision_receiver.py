
import socket


class VisionReceiver:
    def __init__(self, addr, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('', port))
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP,
                             socket.inet_aton(addr) + socket.inet_aton('0.0.0.0'))

        self.sock.settimeout(1.0)

    def receive(self) -> bytes:
        try:
            data, _ = self.sock.recvfrom(2048)
            return data
        except Exception as e:
            print(e)
            print("Failed to receive message from grSim")
