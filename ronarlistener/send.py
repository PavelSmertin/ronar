import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='text')

channel.basic_publish(exchange='', routing_key='text', body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()