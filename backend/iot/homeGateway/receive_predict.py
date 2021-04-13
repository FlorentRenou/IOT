import os
import sys
import pika
import json

def main():
    # Connexion local, on peut le remplacer par une IP ou un nom si on veut une autre machine
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='predict',
                             exchange_type='fanout')

    # Message qu'on souhaite envoyé
    result = channel.queue_declare(queue='', durable=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange='predict', queue=queue_name)

    # définition de la fonction callback
    def callback(ch, method, properties, body):
        print(" [x] Received %r" % json.loads(body))

    # Définition de la queue, on enlève le auto_ack
    channel.basic_consume(queue=queue_name,
                          on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
