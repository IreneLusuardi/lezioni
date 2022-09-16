import json

from secret import mqtt_user,mqtt_password,broker_ip,broker_port,default_topic
import paho.mqtt.client as mqtt
from google.cloud import firestore


def on_connect(client, userdata, flags, rc): #quando si connette si sottoscrive al topic di default
    print("Connected with result code " + str(rc))
    mqtt_client.subscribe(default_topic)
    print("Subscribed to: " + default_topic)

# Define a callback method to receive asynchronous messages
def on_message(client, userdata, message): #viene chiamata la funzione quando arriva un nuovo evento che centra con il topic
    msg = json.loads(str(message.payload.decode("utf-8"))) #lo trasforma in dizionario python tramite json
    db = firestore.Client.from_service_account_json('credentials.json')
    db.collection(msg['sensor']).document(msg['time']).set({'time': msg['time'], 'value': msg['pm10']}) #salva in una tabella di firestore i dati del sensore
    print(msg)


# Configuration variables
client_id = "Consumer2"


# Create a new MQTT Client
mqtt_client = mqtt.Client(client_id)
mqtt_client.on_message = on_message #quando riceve un messaggio chiama la funzione on message
mqtt_client.on_connect = on_connect #si connette al broker mqtt
# Connect to the target MQTT Broker
print('connect',broker_ip, broker_port)
mqtt_client.username_pw_set(username=mqtt_user, password=mqtt_password)
mqtt_client.connect(broker_ip, broker_port)
mqtt_client.loop_forever()