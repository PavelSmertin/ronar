import asyncore, socket, time

class client(asyncore.dispatcher):

    secs = 1
    def __init__(self, host):
        self.host = host
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)

        self.connect((host, 32001))

    def handle_connect(self):
        print ('Connected to', self.host)

    def handle_close(self):
        self.close()

    def handle_write(self):
        print(self.secs)
        time.sleep(self.secs)
        self.send(bytes.fromhex('11 61 3a 00 2b 16 11 11 00 00 00 00 12 34 56 78 9a bc de f0 12 34 56 78 9a bc de f0 00 00 24 00 13 01 15 02 20 19 3b 0e 64 00 31 01 00 00 00 00 00 00 00 00 00 00 7f 00 00 00 00 00 ec 5b 90 99'))

    def handle_read(self):
        print (' ', self.recv(1024))

clients = []
clients.append(client('localhost'))

asyncore.loop()