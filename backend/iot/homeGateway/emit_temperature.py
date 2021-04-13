import pika
import sys
from datetime import datetime

# Connexion local, on peut le remplacer par une IP ou un nom si on veut une autre machine
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='temperature', exchange_type='fanout')

# On définit le exchange, le nom de la queue est spécifié dans le exchange
message = {'temperature': '20°C', 'sensor': 's1', 'timestamp': datetime.now()}
channel.basic_publish(exchange='logs', routing_key='', body=message)

connection.close()
