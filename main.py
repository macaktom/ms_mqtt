import sys

import paho.mqtt.client as mqtt
import time


def setup_client(client):
    client.username_pw_set(username='mobilni', password='Systemy')
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker_address, port=1883)  # connect to broker
    client.loop_start()


def create_user():
    pass


def login():
    pass


def logout():
    pass


def send_message():
    pass


def receive_message():
    pass


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        global Connected  # Use global variable
        Connected = True  # Signal connection
    else:
        print("Connection failed, Returned code {rc}")


def on_message(client, userdata, message):
    print(f'Client {client._client_id} Message received: {message.payload}')


Connected = False
broker_address = "pcfeib425t.vsb.cz"
username1 = "mac0441"
username2 = "mac0441_test"
client1 = mqtt.Client(client_id=username1, clean_session=False)  # create new instance
client2 = mqtt.Client(client_id=username2, clean_session=False)
clients = [client1, client2]
for client in clients:
    setup_client(client)

while Connected != True:  # Wait for connection
    time.sleep(0.1)
client1.subscribe(f"/mschat/all/#")
client1.subscribe(f"/mschat/status/#")
client2.subscribe(f"/mschat/status/#")
client1.publish(f"/mschat/status/{username1}", "online")
client2.publish(f"/mschat/status/{username2}", "online")
client1.publish(f"/mschat/user/{username2}/{username1}", "Test message from client1")
client2.publish(f"/mschat/user/{username1}/{username2}", "Test message from client2")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print('exiting')
    client1.disconnect()
    client1.loop_stop()
    client2.disconnect()
    client2.loop_stop()
    sys.exit()
