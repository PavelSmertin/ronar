import pika

def __logHex(msg):
        return " ".join(["{:02x}".format(x).upper() for x in msg])

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='text')

message = b'\x24\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

channel.basic_publish(
	exchange='', 
	routing_key='text', 
	body=message
)
print(__logHex(message))
connection.close()
