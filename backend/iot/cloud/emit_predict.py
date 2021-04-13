import pika
import sys
import json
from datetime import datetime, timedelta
import pickle

def predict_temperature(name, temperature, timestamp):
    # Connexion local, on peut le remplacer par une IP ou un nom si on veut une autre machine
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='predict', exchange_type='fanout')

    loaded_model = pickle.load(open("model_regressor_"+name,"rb"))
    y_pred = loaded_model.predict(timestamp+timedelta(hours=1))
    new_temperature = temperature
    if y_pred < temperature-0.5 :
        # On doit refroidir
        new_temperature -= 0.2
    elif y_pred > temperature+0.5 : 
        # On doit chauffer
        new_temperature += 0.2

    # On définit le exchange, le nom de la queue est spécifié dans le exchange
    message = {'temperature': new_temperature, 'sensor': name}
    channel.basic_publish(exchange='predict', routing_key='', body=json.dumps(message))

    connection.close()
