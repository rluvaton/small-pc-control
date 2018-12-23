# Imports
import socket

# Saving images
import os

from responseHandle import ResponseHandler

target_ip = '127.0.0.1'
target_port = 9999
size = 4096

# create an ipv4 (AF_INET) socket object using the tcp protocol (SOCK_STREAM)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print 'Connecting...'

# connect the server
# server.connect((target, port))
server.connect((target_ip, target_port))

print 'Connection {}:{} Established'.format(target_ip, target_port)
print 'You Can Start Typing...'

message = None
data = None


# Create Directory if not exist
def create_dir_if_not_exists(dir_name):
    try:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        return True
    except Exception, err:
        print 'Error at create directories: ', err
        return False


# Server Name
server_name = None


while True:
    # ask the server whether he wants to continue
    message = raw_input("> ")
    print 'send: {}'.format(message)

    if not server:
        print 'Server Disconnected'
        break

    res = ResponseHandler.get_request_type(message)
    if res[1] is None:
        # Message sent to server
        server.send(message)

        # Message received from server
        data = server.recv(size)

        ResponseHandler.handle_requests(message,
                                        data,
                                        lambda _size: server.recv((size if _size is None else _size)),
                                        lambda _mess: server.send(_mess))

        # Print the received message
        print 'Received: {}'.format(data)
    else:
        print 'Error Accord: {}'.format(res[1])
        continue

server.close()
