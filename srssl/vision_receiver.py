
import socket


class VisionReceiver:
    def __init__(self, addr, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((addr, port))

        self.sock.settimeout(1.0)

    def receive(self) -> bytes:
        try:
            data, _ = self.sock.recvfrom(2048)
            return data
        except Exception as e:
            print(e)
            print("Failed to receive message from vision system.")
