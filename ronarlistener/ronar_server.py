import asyncio
import logging

from rabbit_consumer import RabbitConsumer

from incoming import Incoming


class RonarServer(object):
    
    def __init__(self, host, port, loop=None):
        self._loop = loop or asyncio.get_event_loop() 
        self._server = asyncio.start_server(self.handle_connection, host=host, port=port)
        self._writer = None

    
    def start(self, and_loop=True):
        self._server = self._loop.run_until_complete(self._server)
        logging.info('Listening established on {0}'.format(self._server.sockets[0].getsockname()))
        self.run_consumer()
        if and_loop:
            self._loop.run_forever()

    def run_consumer(self):
        amqp_url = 'amqp://localhost:5672/%2F'
        consumer = RabbitConsumer(amqp_url)
        consumer.run(self.on_message)

    def stop(self, and_loop=True):
        self._server.close()
        if and_loop:
            self._loop.close()
        print('server closed')
     
    async def handle_connection(self, reader, writer):
        self._writer = writer
        logging.info('Socket started')
        while True:
            data = await reader.read(1024)
            message = data
            addr = writer.get_extra_info('peername')
            print("Request %r from %r" % ("", addr))            
            print("Response sent: %r" % message)

            incoming = Incoming(message)

            writer.write(incoming.getResponse())
            await writer.drain()
            if not data:
                break  # EOF



    def on_message(self):
        message = "Команда"
        logging.info('handle_queue started')

        if self._writer:
            self._writer.write(message.encode())
            self._writer.drain()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    server = RonarServer('', 32001)
    try:
        server.start()
    except KeyboardInterrupt:
        pass # Press Ctrl+C to stop
    finally:
        server.stop()