import paho.mqtt.client as mqtt
import time

def on_message(client, userdata, message):
	#print("message received", str(message.payload.decode("utf-8")))
	print("message topic=", message, topic)
	#print("message retain flag=",message.retain)
	
broker="m20.cloudmqtt.com"
port=17731
username="tvpgffmb"
password="hIHVIrRFJxmm"

client = mqtt.Client("P1")
client
client.on_message = on_message

client.username_pw_set(username,password)

client.connect(broker,port)
client.subscribe("ADC0/#")
client.subscribe("MCP_PORTB/#")
client.loop_start()
client.loop_stop()
