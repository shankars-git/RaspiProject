#!/usr/bin/python
from sense_hat import SenseHat
import socket
import logging
from time import sleep
try:
    import thread
except ImportError:
    import _thread as thread

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

sense = SenseHat()

sense.set_imu_config(True, True, True)

orientation = None
def orientation_thread():
    global orientation
    global ap
    while(True):
        orientation = sense.get_orientation()

host = 'localhost'
port = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (host, port)

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address)
server_socket.listen(5)

thread.start_new_thread(orientation_thread, ())

try:
    while True:
        client_socket, client_address = server_socket.accept()
        logger.info(f"Accepted connection from {client_address}")
        
        try:
            while True:
                o = sense.get_orientation()
                pitch = o["pitch"]
                roll = o["roll"]
                yaw = o["yaw"]
                print("yaw = {0:.2f}; pitch = {1:.2f}; roll = {2:.2f}".format(orientation["yaw"], orientation["pitch"], orientation["roll"]))
                message = f"{orientation['yaw']} {orientation['pitch']} {orientation['roll']}"
                print(message)
                client_socket.send(message.encode('utf-16'))
                sleep(0.5)
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
