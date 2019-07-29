import pika

from incoming import Incoming

import logging
log = logging.getLogger(__name__)


def __logHex(msg):
        return " ".join(["{:02x}".format(x).upper() for x in msg])

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='text')

incoming = Incoming()

message = incoming.getResponseHead(True)

channel.basic_publish(
	exchange='', 
	routing_key='text', 
	body=message
)
print(__logHex(message))
connection.close()
