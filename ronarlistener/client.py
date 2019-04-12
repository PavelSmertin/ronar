import asyncore, socket, time

class client(asyncore.dispatcher):

    secs = 0
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
        self.secs = self.secs + 1
        time.sleep(self.secs)
        self.send('6E3E0053"RO-TEM"4894L0#355911044259579[1210 18 00 28 03EB92151D1D FEB6]_04:24:05,12-13-2017'.encode('utf8'))

    def handle_read(self):
        print (' ', self.recv(1024))

clients = []
clients.append(client('localhost'))

asyncore.loop()