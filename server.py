# Imports
import socket
import threading
import time
from threading import Timer

from userManagement import compute_MD5_hash
from isAlive import HeartBeat
from user import User

bind_ip = '0.0.0.0'
bind_port = 9999
bind_heartbeat_port = 9998

# Local host
bind_ip = '127.0.0.1'

size = 4096

# region Requests Server
# Create Socket
server = None

# endregion

# region Heartbeat Server

# Create Heartbeat Socket
heartbeat_server = None
is_alive = None  # type: HeartBeat
# endregion

users = {

}  # type: Dict[str, User]

# Listen Info
print 'Listening on {}:{}'.format(bind_ip, bind_port)

print 'Heartbeat: Listening on {}:{}'.format(bind_ip, bind_heartbeat_port)


# Init Main Server
def init_main_server():
    global server

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((bind_ip, bind_port))
    server.listen(5)  # max backlog of connections


# Init Heartbeat Server
def init_heartbeat_server():
    global heartbeat_server

    heartbeat_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    heartbeat_server.bind((bind_ip, bind_heartbeat_port))
    heartbeat_server.listen(5)  # max backlog of connections


def heartbeat_timeout_end(user):
    # type: (User) -> None
    """
    Handler when user didn't response to the heartbeat
    :param user: user that his timeout ended
    """

    print 'Connection to remote expired'
    user.close()


def heartbeat_send(user, message):
    # type: (User, str) -> None
    """
    Send Message Callback to HeartBeat
    :param user: User that need to send to
    :param message: Message to sent
    """
    user.send(message, False)


def heartbeat_user_handler(is_alive, user_socket):
    # type: (HeartBeat, socket.socket) -> None
    """
    New User Connection Handler
    :param is_alive: Heartbeat class instance
    :param user_socket: User socket that connected
    """
    user = User(None, user_socket)  # type: User

    # Do MD5 on the current timestamp and use it as the auth token
    auth_token = compute_MD5_hash(str(time.time()))

    # Send the auto token to the user
    user.send(auth_token, False)

    # Add the auth token as the key, while the value is the user itself
    # (this give me O(1) because I'll get the auth token from the user)
    users[auth_token] = user

    # Insert the user to the heartbeat
    is_alive.add(user)


def run_heartbeat():
    """
    Start Heartbeat Server
    """
    global is_alive
    is_alive = HeartBeat('HB', 'T', heartbeat_send, 5, 10, heartbeat_timeout_end)

    # Start The Server
    while True:
        heartbeat_client_sock, heartbeat_address = heartbeat_server.accept()

        print 'Accepted connection from {}:{}'.format(heartbeat_address[0], heartbeat_address[1])
        heartbeat_client_handler = threading.Thread(
            target = heartbeat_user_handler,
            args = (is_alive, heartbeat_client_sock,)
        )
        heartbeat_client_handler.start()


init_heartbeat_server()
init_main_server()

# Start running the heartbeat
threading.Thread(
    target = run_heartbeat,
    args = ()
    # without comma you'd get error:
    # Error: a... TypeError: handle_client_connection() argument after * must be a sequence, not _socketobject
).start()


# New Client Connection Handler
def handle_client_connection(client_socket):
    # type: (socket.socket) -> None

    # Receive data from client
    auth_token = client_socket.recv(size)

    if auth_token not in users:
        err_msg = 'Invalid Auth Token, exiting...'
        print err_msg
        client_socket.send(err_msg)
        client_socket.close()
        return

    # Send Ready Message for the client to start his application
    client_socket.send('I\'m ready')

    user = users[auth_token]  # type: User

    # Remove the auto token from the users dictionary
    users[auth_token] = None

    # Set this socket as it's main socket (the socket for all the requests)
    user.set_main_socket(client_socket)

    # Insert the user to the heartbeat
    # is_alive.add(user)

    while True:
        try:
            # Receive data from client
            request = user.receive(size, True)

            # Check if disconnected
            if not request:
                print 'Client Disconnected'
                break

            print 'Received | {}'.format(request)

            res = user.user_actions.handle_requests(
                request)  # type: {'message': str, 'close-client': bool, 'error': str}

            response = None

            if 'error' in res:
                response = res['error']
                print 'Error occurred: {}'.format(res['error'])
            else:
                response = res['message']
                print 'Send     | {}'.format(res['message'])

            # Response to client
            user.send(response, True)

            print ' ------------------- '

            if 'stop-heartbeat' in res and res['stop-heartbeat']:
                is_alive.remove(user)
                # user.close()

                def response_limit_passed_callback():
                    is_alive.response_limit_passed_callback(user)

                # Set timer to run until the response timeout (as requested in the exercise)
                Timer(is_alive.response_limit_timeout, response_limit_passed_callback).start()
                break

            # Close client
            elif 'close-client' in res and res['close-client']:
                is_alive.remove(user, True)
                user.close()
                break
        except Exception, e:
            user.close()
            print 'Error occurred', e
            print 'Closing'
            break


# Start Running The Request Server
while True:
    client_sock, address = server.accept()
    print 'Accepted connection from {}:{}'.format(address[0], address[1])
    client_handler = threading.Thread(
        target = handle_client_connection,
        args = (client_sock,)
        # without comma you'd get error:
        # Error: a... TypeError: handle_client_connection() argument after * must be a sequence, not _socketobject
    )
    client_handler.start()
