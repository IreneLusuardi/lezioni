# For this example we rely on the Paho MQTT Library for Python
# You can install it through the following command: pip install paho-mqtt
import json
from secret import mqtt_user,mqtt_password,broker_ip,broker_port,default_topic
import paho.mqtt.client as mqtt
import time

#Produttore
# Configuration variables
client_id = "sensor2" #associato al sensore 2

#si connette al broker
mqtt_client = mqtt.Client(client_id)
print("Connecting to "+ broker_ip + " port: " + str(broker_port))
mqtt_client.username_pw_set(username=mqtt_user, password=mqtt_password)
mqtt_client.connect(broker_ip, broker_port)

mqtt_client.loop_start()

with open('CleanData_PM10.csv') as f: #legge il file
    for r in f:
        r = r.strip()
        t,pm10 = r.split(',')
        pm10 = float(pm10)
        payload_string = json.dumps({'sensor':client_id,'time':t,'pm10':pm10})
        infot = mqtt_client.publish(default_topic, payload_string) #invia le info al broker mqtt che lo smisterà a tutti i potenziali consumatori dell'evento
        infot.wait_for_publish() #vpn per bypassare il firewall di unimore
        print('message sent',t)
        time.sleep(10)

mqtt_client.loop_stop()