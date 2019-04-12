"""
Handles receiving of the alarm notification messages on the TCP/IP socket
"""
__author__ = 'Pashtet <pashtetbezd@gmail.com>'

import logging
import socketserver
from datetime import datetime
import time
from enum import Enum
from ronarlistener.message import Message, Protocol

log = logging.getLogger(__name__)
TIME_INTERVAL = 40


class AlarmNotificationHandler(socketserver.StreamRequestHandler):

    timeout = 180

    def handle(self):

        try: 
            while True:
                line = self.request.recv(1024).strip().decode('utf8')

                message = Message(line)
                response = message.getResponse()

                if response is None:
                    self.request.close()
                    return

                # Сохраняем только подтвержденные ответы ACK
                if message.protocol_out is Protocol.ACK:
                    self.server.event_store.store_event(message)

                log.info("Response: " + response)

                self.request.sendall(response.encode('utf8'))

                if not line:
                    break

        except OSError as error:
            log.warn('Got error while reading from socket {}'.format(error.args[0]), exc_info=error)
        finally:
            self.request.close()
