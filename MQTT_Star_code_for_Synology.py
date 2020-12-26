import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from time import sleep
from star import Star

import threading
import random

# importing enum for enumerations 
from enum import Enum 
  
# creating enumerations using class 
class Direction(Enum): 
    Clockwise = 1
    Anticlockwise = 2
    
star = Star(pwm=True)
leds = star.leds

MQTT_BROKER_SERVER = "192.168.178.142"
MQTT_BROKER_PORT = 1883
MQTT_username = "jb"
MQTT_password = "test"
MQTT_PATH = "STAR1"

 # WORKS
step_default = 0.5
reducer = 0.95
direction = Direction.Clockwise

current_iteration = 0
number_of_iterations_to_do = 2

step = 1
run_up = True

count = 1 # 0 sets the inner LEDs on
current_iteration = 0

# def Starpattern1():
#  
#     # WORKS
#     step_default = 0.5
#     reducer = 0.95
#     direction = Direction.Clockwise
# 
#     current_iteration = 0
#     number_of_iterations_to_do = 2
# 
#     step = 1
#     run_up = True
#     
#     count = 1 # 0 sets the inner LEDs on
#     current_iteration = 0
#     direction = Direction.Clockwise
#     step = step_default
#     star.off()
# 
#     while (current_iteration < number_of_iterations_to_do):
#         completed = False
#         while (completed==False):
#     
#             if(count%26!=0):
#                 leds[count%26].on()
#                 sleep(step)
#                 leds[count%26].off()
#                 
#             count += 1
#             step = step*reducer
#             
#             if(step <= 0.0001):
#                 star.outer.pulse(fade_in_time=0.5,fade_out_time=0.5,n=5)
#                 star.inner.pulse(fade_in_time=0.5,fade_out_time=0.5,n=5)
#                
#                 sleep(5)
#                 count = 0
#                 step = 1
# 
#                 completed = True
#             
#         current_iteration += 1
        
class myThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        
        self.threadID = threadID
        self.name = name
        self._running = True
      
    def terminate(self): 
        self._running = False
        
    def run(self):
        print("Starting " + self.name)
        # Get lock to synchronize threads
        threadLock.acquire()

        star.off()

        while ((current_iteration < number_of_iterations_to_do) and self._running):
            completed = False
            while (completed==False and self._running):
    
                if(count%26!=0):
                    leds[count%26].on()
                    sleep(step)
                    leds[count%26].off()
                
                count += 1
                step = step*reducer
            
                if(step <= 0.0001):
                    star.outer.pulse(fade_in_time=0.5,fade_out_time=0.5,n=5)
                    star.inner.pulse(fade_in_time=0.5,fade_out_time=0.5,n=5)
               
                    sleep(5)
                    count = 0
                    step = 1

                    completed = True
            
            current_iteration += 1

        threadLock.release()
      
# def print_time(threadName, delay, counter):
#    while counter:
#       time.sleep(delay)
#       print "%s: %s" % (threadName, time.ctime(time.time()))
#       counter -= 1
      
threadLock = threading.Lock()
threads = []

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    publish.single(MQTT_PATH,"STAR1 Connected", hostname = MQTT_BROKER_SERVER)
    client.subscribe(MQTT_PATH)
    
def on_message(client, userdata, message):
    topic = message.topic
    message = str(message.payload.decode("utf-8"))
    print("*** Message Topic=", topic)
    print("    message received", message)
    
    if (topic == "STAR1"):
        do_pattern(message)
        
def do_pattern(pat):
    print("Doing Pattern",pat)
    if (pat=="1"):
        thread1 = myThread(1, "1", 1)
        threads.append(thread1)
        threads[0].start()

    if (pat=="2"):
        star.outer.pulse()
    if (pat=="off"):
        star.off()
        threads[0].terminate()
        del threads[0]
        
        #thread1.terminate()
  

    #print("message retain flag=",message.retain)



client = mqtt.Client("P1")
client
client.on_message = on_message
client.on_connect = on_connect

client.username_pw_set(MQTT_username,MQTT_password)

client.connect(MQTT_BROKER_SERVER,MQTT_BROKER_PORT)
    
#client.subscribe("TEST")
client.subscribe("TEST/TEST1")
client
client.subscribe("ADC0/#")
client.subscribe("MCP_PORTB/#")
for numbers in range(4):
    publish.single(MQTT_PATH,"Hello from Pi..."+str(numbers), hostname = MQTT_BROKER_SERVER)
    sleep(2)
#client
client.loop_start()
#client.loop_stop()
