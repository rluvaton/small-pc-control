# Imports
import socket

target_ip = '127.0.0.1'
target_port = 9999

# create an ipv4 (AF_INET) socket object using the tcp protocol (SOCK_STREAM)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect the server
# server.connect((target, port))
server.connect((target_ip, target_port))

while True:

    # ask the server whether he wants to continue
    message = raw_input("> ")
    print 'send: {}'.format(message)

    if not server:
        print 'Server Disconnected'
        break

    # message sent to server
    server.send(message)

    # message received from server
    data = server.recv(4096)

    # print the received message
    # here it would be a reverse of sent message
    print 'Received: {}'.format(data)

server.close()
