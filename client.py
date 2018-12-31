# Imports
import socket
import threading

from responseHandle import ResponseHandler
from utils import *
from heartbeat import Heartbeat

target_ip = '127.0.0.1'

# region Main Server

# The Server
server = None

target_port = 9999

# endregion

# region Heartbeat variables


# The server
target_heartbeat_port = 9998

# The request the server sent to client every 5 seconds
heartbeat_request_ms = 'HB'

# The response of client after each heartbeat
heartbeat_response_ms = 'T'

is_heartbeat_connected = True


def get_is_heartbeat_connected():
    return is_heartbeat_connected


def set_is_heartbeat_connected(value):
    global is_heartbeat_connected
    is_heartbeat_connected = value


heartbeat = Heartbeat(target_ip, target_heartbeat_port, heartbeat_response_ms, heartbeat_request_ms, 10,
                      get_is_heartbeat_connected, set_is_heartbeat_connected)

# endregion

# Buffer Size
size = 4096

if request_valid_response("Custom IP ?", 'y', 'n'):
    target_ip = raw_input("Your IP Is: ").strip()


# Init Server - Declare, Connect and wait for ready
def init_server(unique):
    global server

    # create an ipv4 (AF_INET) socket object using the tcp protocol (SOCK_STREAM)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print '\tServer:'
    print '\t\tConnecting...'

    # connect the server
    # server.connect((target, port))
    server.connect((target_ip, target_port))

    print '\t\tConnection {}:{} Established'.format(target_ip, target_port)
    print '\t\tSending Unique Auth token to main server'
    server.send(unique)
    print '\t\tToken Sent, wait for sign to get started'

    # Server Ready Message
    server_init_ms = 'I\'m ready'

    # Set Timeout until the server returns that he is ready
    server_ready_timeout = 5
    server.settimeout(server_ready_timeout)

    server.recv(get_string_size(server_init_ms))

    # Remove timeout
    server.settimeout(None)

    print '\t\tServer Ready'

    print '\nYou Can Start Typing...'


print 'Initializing...'
init_server(heartbeat.connect())

# Create Thread of the run heartbeat
threading.Thread(
    target = heartbeat.run,
    args = ()
    # without comma you'd get error:
    # Error: a... TypeError: handle_client_connection() argument after * must be a sequence, not _socketobject
).start()

while True:
    # ask the server whether he wants to continue
    message = raw_input("> ")
    print 'send: {}'.format(message)

    if not server:
        print 'Server Disconnected'
        break

    handler = ResponseHandler(lambda _size: server.recv((size if _size is None else _size)),
                              lambda _mess: server.send(_mess))

    # Message sent to server
    server.send(message)

    # Message received from server
    data = server.recv(size)

    fn_res = handler.handle_requests(message, data)

    # Print the received message
    print 'Received: {}'.format(data)

    if 'close-client' in fn_res and fn_res['close-client']:
        is_heartbeat_connected = False
        break

    if 'error' in fn_res:
        print 'Error', fn_res
        break

server.close()
