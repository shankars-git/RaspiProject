#!/usr/bin/python
from beebotte import *
import socket
import logging
from time import sleep
from sense_hat import SenseHat

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

sense = SenseHat()
sense.clear()

white = (255,255,255)

# Server configuration
host = 'localhost' 
port = 12345
sleep(5)
# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

### API_KEY and SECRET_KEY associated with my account
bbt = BBT('XoYx21WaqQ7ZI1VSm8aoBAZf', 'etVrrYBf6D8K7cdTdfvq190feC29OufF')


### Create resources channel name and resource names
yaw_resource   = Resource(bbt, 'Yaw_Pitch_Roll', 'Yaw')
pitch_resource  = Resource(bbt, 'Yaw_Pitch_Roll', 'Pitch')
roll_resource   = Resource(bbt, 'Yaw_Pitch_Roll', 'Roll')

roll_threshold = 5
yaw_threshold = 150
pitch_threshold = 350

try:
    # Connect to the server
    client_socket.connect((host, port))
    prev_yaw = 0.0
    prev_pitch = 0.0
    prev_roll = 0.0

    while True:
        # Receive data from the server (assuming the server sends text messages)
        data = client_socket.recv(1024)  # Receive up to 1024 bytes of data
        if not data:
            break
        temp = data.decode('utf-16')
        parts = temp.split()
        print(parts)
        try:
            yaw = float(parts[0])
            pitch = float(parts[1])
            roll = float(parts[2])
            yaw_difference = yaw - prev_yaw
            prev_yaw = yaw
            pitch_difference = pitch - prev_pitch
            prev_pitch = pitch
            roll_difference = roll - prev_roll
            prev_roll = roll
            print("yaw = {0:.2f}; pitch = {1:.2f}; roll = {2:.2f}".format(yaw,pitch,roll))
            yaw_resource.write(yaw)
            #pitch_resource.write(pitch)
            #roll_resource.write(roll)
            if (yaw_difference > 10.0 or pitch_difference > 10.0 or yaw_difference > 10) :
              sense.show_letter("X", white)
            else :
              sense.clear()

        except ValueError as e:
            logger.error(f"Error parsing data: {e}")

except KeyboardInterrupt:
    print("Client stopped.")
except ConnectionRefusedError:
    print("Connection to the server was refused.")
except Exception as e:
    print(f"Error: {e}")
finally:
    # Close the client socket
    client_socket.close()
