import RPi.GPIO as GPIO
import time
LedPin = 26 # pin11
def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LedPin, GPIO.OUT)
    GPIO.output(LedPin, GPIO.LOW)
# def blink():
#     while True:
#         GPIO.output(LedPin, GPIO.HIGH) # led on
#         time.sleep(0.5)
#         GPIO.output(LedPin, GPIO.LOW) # led off
#         time.sleep(1)
def destroy():
    GPIO.output(LedPin, GPIO.LOW) # led off
    GPIO.cleanup() # Release resource
import socket
HOST = '192.168.2.135'
PORT = 80
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
#sock.connect((HOST, PORT))  
online = True
setup()
def push():
    GPIO.output(LedPin, GPIO.HIGH) # led on
    time.sleep(0.5)
    GPIO.output(LedPin, GPIO.LOW) # led off
    time.sleep(0.5)
while 1:
    try: 
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        re_mes=sock.recv(1024).decode()
        #connection.close()
        sock.close()
        if re_mes=="Online":
            if not online:
                push()
                online = True
        elif re_mes=="Offline":
            if online:
                push()
                online = False
        print(re_mes)
    except KeyboardInterrupt:
        destroy()
        sock.close() 
