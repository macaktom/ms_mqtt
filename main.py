import paho.mqtt.client as mqtt
import time


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        global Connected  # Use global variable
        Connected = True  # Signal connection
    else:
        print("Connection failed, Returned code {rc}")


def on_message(client, userdata, message):
    print(f'Client {client} Message received: {message.payload}')


Connected = False
broker_address = "pcfeib425t.vsb.cz"
client = mqtt.Client("client1")  # create new instance
client.username_pw_set(username='mobilni', password='Systemy')
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address, port=1883)  # connect to broker
client2 = mqtt.Client("client2")  # create new instance
client2.username_pw_set(username='mobilni', password='Systemy')
client2.on_connect = on_connect
client2.on_message = on_message
client2.connect(broker_address, port=1883)
# client.publish("/mschat/user/id_příjemce/id_odesilatele","OFF")#publish
client.loop_start()
client2.loop_start()
while Connected != True:  # Wait for connection
    time.sleep(0.1)
client.subscribe("/mschat/#")
client2.subscribe("/mschat/#")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print('exiting')
    client.disconnect()
    client.loop_stop()
    client2.disconnect()
    client2.loop_stop()