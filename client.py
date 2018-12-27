# Imports
import socket
import threading

from responseHandle import ResponseHandler
from utils import *

target_ip = '127.0.0.1'

# region Main Server

# The Server
server = None

target_port = 9999

# endregion

# region Heartbeat variables

# The server
heartbeat_server = None

target_heartbeat_port = 9998

# The request the server sent to client every 5 seconds
heartbeat_request_ms = 'HB'
heartbeat_request_byte_size = get_string_size(heartbeat_request_ms)

# The response of client after each heartbeat
heartbeat_response_ms = 'T'

heartbeat = True

# endregion

# Buffer Size
size = 4096

if request_valid_response("Custom IP ?", 'y', 'n'):
    target_ip = raw_input("Your IP Is: ").strip()


# region Heartbeat Functions

# Init Heartbeat Server
def init_heartbeat():
    """
    Init Heartbeat Server
    :return: The unique key to start connecting with the main server
    :type: () -> str
    """
    global heartbeat_server

    # create an ipv4 (AF_INET) socket object using the tcp protocol (SOCK_STREAM)
    heartbeat_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print '\tHeartbeat Server:'
    print '\t\tConnecting...'

    # connect the server
    heartbeat_server.connect((target_ip, target_heartbeat_port))

    print '\t\tConnection {}:{} Established'.format(target_ip, target_heartbeat_port)
    print '\t\tGetting Unique Auth Token...'

    # Set Timeout until the server returns the token
    heartbeat_token_timeout = 7
    heartbeat_server.settimeout(heartbeat_token_timeout)

    token = heartbeat_server.recv(size)

    # Remove the timeout
    heartbeat_server.settimeout(None)

    print 'Token', token

    return token


def run_heartbeat():
    global heartbeat

    heartbeat_request_timeout = 10
    heartbeat_server.settimeout(heartbeat_request_timeout)
    try:
        # Message received from server
        heartbeat_server.recv(heartbeat_request_byte_size)
    except socket.timeout, e:
        heartbeat = False
        print 'Connection Closed (Heartbeat)'

    heartbeat_request_timeout = 10
    while heartbeat:
        try:
            # Message received from server
            heartbeat_server.recv(heartbeat_request_byte_size)
        except socket.timeout, e:
            print e
            if heartbeat:
                print 'Connection was closed'
            break

        # Message sent to server
        heartbeat_server.send(heartbeat_response_ms)

    heartbeat_server.close()


# endregion


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
init_server(init_heartbeat())

# Create Thread of the run heartbeat
threading.Thread(
    target = run_heartbeat,
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
        heartbeat = False
        break

    if 'error' in fn_res:
        print 'Error', fn_res
        break

server.close()
