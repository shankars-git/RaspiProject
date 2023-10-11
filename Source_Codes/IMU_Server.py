#!/usr/bin/python
from sense_hat import SenseHat
import socket
import logging
from time import sleep
try:
    import thread
except ImportError:
    import _thread as thread

#Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


#Create Object to use SenseHat Library API's
sense = SenseHat()

#Configure the IMU
sense.set_imu_config(True, True, True)

orientation = None

# Function to get the sensor value from SenseHat in Radians
def orientation_thread():
    global orientation
    while(True):
        orientation = sense.get_orientation()

#Server Configaration
host = 'localhost'
port = 12345

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (host, port)

#Binding the socket and release the socket properly if the application is terminated
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address)
server_socket.listen(5)

#Creating a thread to get the sensor data from SenseHat
thread.start_new_thread(orientation_thread, ())

try:
    while True:
        #Wait for the Client to Connect to the server
        client_socket, client_address = server_socket.accept()
        logger.info(f"Accepted connection from {client_address}")
        
        try:
            while True:
                #Get the Orientation data from the thread
                print("yaw = {0:.2f}; pitch = {1:.2f}; roll = {2:.2f}".format(orientation["yaw"], orientation["pitch"], orientation["roll"]))
                #Pack the data in a frame to be sent to Client
                message = f"{orientation['yaw']} {orientation['pitch']} {orientation['roll']}"
                #Send the data to Client
                client_socket.send(message.encode('utf-16'))
                sleep(0.1)
        #Error and Exception Handling
        except KeyboardInterrupt:
            logger.info("Server stopped.")
            break
        except Exception as e:
            logger.error(f"Error: {e}")
        finally:
            if not client_socket._closed:
                client_socket.close()
except KeyboardInterrupt:
    logger.info("Server terminated.")
finally:
    server_socket.close()
