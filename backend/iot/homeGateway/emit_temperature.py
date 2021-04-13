import pika
import sys
import json
from datetime import datetime

# Connexion local, on peut le remplacer par une IP ou un nom si on veut une autre machine
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='temperature', exchange_type='fanout')

# On définit le exchange, le nom de la queue est spécifié dans le exchange
message = {'temperature': '20', 'sensor': 's1', 'timestamp': datetime.now().__str__()}
channel.basic_publish(exchange='temperature', routing_key='', body=json.dumps(message))

connection.close()
