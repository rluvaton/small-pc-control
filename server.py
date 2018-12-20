# Imports
import socket
import threading

from userActions import UserActions

bind_ip = '127.0.0.1'
bind_port = 9999

size = 4096

# Create Socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(5)  # max backlog of connections

# Listen Info
print 'Listening on {}:{}'.format(bind_ip, bind_port)


# New Client Connection Handler
def handle_client_connection(client_socket):
    while True:
        try:
            # Receive data from client
            request = client_socket.recv(size)

            # Check if disconnected
            if not request:
                print 'Client Disconnected'
                break

            print 'Received | {}'.format(request)

            from userActions import UserActions
            res = UserActions.handle_requests(request)
            print 'Send     | {}'.format(res[0])

            # Response to client
            client_socket.send(res[0])

            print ' ------------------- '

            # Close client
            if res[1]:
                client_socket.close()
                break
        except Exception, e:
            client_socket.close()
            print 'Error accord', e
            print 'Closing'
            break


# Start The Server
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
