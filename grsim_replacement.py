import socket


class GrSimReplacement:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self, msg):
        try:
            self.sock.sendto(msg, (self.host, self.port))
            print("Sent message to grSim")
        except Exception as e:
            print(e)
            print("Failed to send message to grSim")
