import asyncio
import logging
import redis

from rabbit_consumer import RabbitConsumer

from incoming import Incoming

class RonarServer(object):
    
    def __init__(self, host, port, loop=None):
        self._loop = loop or asyncio.get_event_loop() 
        self._server = asyncio.start_server(self.handle_connection, host=host, port=port)
        self._writer = None
        self._store = redis.Redis(host='localhost', port=6379)

    
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
            if not data:
                break  # EOF
                
            message = data
            addr = writer.get_extra_info('peername')

            print("Incoming %r from %r" % ("", addr))            
            incoming = Incoming(message)

            if incoming.is_response():
                self._store.hset("out", b'\xFF' + incoming.get_message_id(), message)
                continue
            else:
                self._store.hset("in", b'\x00' + incoming.get_message_id(), message)


            print("Response sent: %r" % message)
            writer.write(incoming.get_response())
            await writer.drain()
            self._store.hset("in", b'\xFF' + incoming.get_message_id(), incoming.get_response())


    def on_message(self, message, tag):
        logging.info('on_message')

        incoming = Incoming()
        message_id = incoming.get_id_from_tag(tag)
        command = incoming.get_response_from(
            message_id = message_id, 
            message_type = b'\x10', 
            command = b'\x24\x00', 
            options = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            )

        print(command)


        if self._writer:
            self._writer.write(command)
            self._writer.drain()
            self._store.hset("out", b'\x00' + message_id, command)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    server = RonarServer('', 32001)
    try:
        server.start()
    except KeyboardInterrupt:
        pass # Press Ctrl+C to stop
    finally:
        server.stop()