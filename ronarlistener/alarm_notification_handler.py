"""
Handles receiving of the alarm notification messages on the TCP/IP socket
"""
__author__ = 'Pashtet <pashtetbezd@gmail.com>'

import logging
import socketserver
from datetime import datetime
import time
from enum import Enum
from ronarlistener.incoming import Incoming
from ronarlistener.rabbit_consumer import RabbitConsumer


log = logging.getLogger(__name__)
TIME_INTERVAL = 40


class AlarmNotificationHandler(socketserver.StreamRequestHandler):

    timeout = 180

    def handle(self):


        #self.request.sendall(b"test")
        #amqp_url = 'amqp://localhost:5672/%2F'
        #consumer = RabbitConsumer(amqp_url)
        #consumer.run()

        try: 
            while True:
                line = self.request.recv(1024)

                log.info(line.hex())

                incoming = Incoming(line)
                #response = incoming.getResponse()

                # if response is None:
                #     self.request.close()
                #     return

                #log.info('AlarmNotificationHandler')
                #log.info(vars(incoming))
                self.server.event_store.store_event(incoming)

                #log.info("Response: " + response)

                #self.request.sendall(response.encode('utf8'))

                if not line:
                    break

        except OSError as error:
            log.warn('Got error while reading from socket {}'.format(error.args[0]), exc_info=error)
        finally:
            self.request.close()
