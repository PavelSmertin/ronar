import asyncio
import logging

class RonarServer(object):
    
    def __init__(self, host, port, loop=None):
        self._loop = loop or asyncio.get_event_loop() 
        self._server = asyncio.start_server(self.handle_connection, host=host, port=port)
    
    def start(self, and_loop=True):
        self._server = self._loop.run_until_complete(self._server)
        logging.info('Listening established on {0}'.format(self._server.sockets[0].getsockname()))
        if and_loop:
            self._loop.run_forever()
    
    def stop(self, and_loop=True):
        self._server.close()
        if and_loop:
            self._loop.close()
        print('server closed')
     
    async def handle_connection(self, reader, writer):
        self._loop.create_task(self.handle_socket(reader, writer)),
        self._loop.create_task(self.handle_queue(reader, writer)),

    async def handle_socket(self, reader, writer):
        logging.info('Socket started')
        while True:
            data = await reader.read(1024)
            message = data
            addr = writer.get_extra_info('peername')
            print("Request %r from %r" % ("", addr))            
            print("Response sent: %r" % message)
            message = "Ответ"
            writer.write(message.encode())
            await writer.drain()
            if not data:
                break  # EOF

    async def handle_queue(self, reader, writer):
        logging.info('Command waiting started')
        await asyncio.sleep(5)
        print("Command sent")
        message = "Команда"
        writer.write(message.encode())
        await writer.drain()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    server = RonarServer('', 32001)
    try:
        server.start()
    except KeyboardInterrupt:
        pass # Press Ctrl+C to stop
    finally:
        server.stop()