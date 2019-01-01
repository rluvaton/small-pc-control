import socket
from utils import get_string_size

is_connected = True


def get_is_connected_default():
    return is_connected


def set_is_connected_default(value):
    global is_connected
    is_connected = value


class Heartbeat(object):
    heartbeat_server = None  # type: socket.socket

    def __init__(self, ip, port, client_response_ms, server_request_ms, server_request_timeout = 10, get_is_connected = get_is_connected_default,
                 set_is_connected = set_is_connected_default, token_size = 4096,
                 token_timeout = 10):
        self.ip = ip
        self.port = port

        self.token_size = token_size
        self.token_timeout = token_timeout

        self.client_res_ms = client_response_ms

        self.server_req_ms = server_request_ms

        self.server_req_size = get_string_size(self.server_req_ms)
        self.server_req_timeout = server_request_timeout

        self.get_is_connected = get_is_connected
        self.set_is_connected = set_is_connected

        self.heartbeat_server = None

        self.socket_offline = False

    # Init Heartbeat Server
    def connect(self):
        """
        Init Heartbeat Server
        :return: The unique key to start connecting with the main server
        :type: () -> str
        """
        # create an ipv4 (AF_INET) socket object using the tcp protocol (SOCK_STREAM)
        self.heartbeat_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        print 'Heartbeat Server:'
        print '\tConnecting...'

        # connect the server
        self.heartbeat_server.connect((self.ip, self.port))

        print '\tConnection {}:{} Established'.format(self.ip, self.port)
        print '\tGetting Unique Auth Token...'

        # Set Timeout until the server returns the token
        self.heartbeat_server.settimeout(self.token_timeout)

        token = self.heartbeat_server.recv(self.token_size)

        # Remove the timeout
        self.heartbeat_server.settimeout(None)

        print 'Token', token

        return token

    def run(self):
        self.heartbeat_server.settimeout(self.server_req_timeout)
        try:
            if not self.socket_offline:
                # Message received from server
                self.heartbeat_server.recv(self.server_req_size)
        except socket.timeout, e:
            if not self.socket_offline:
                self.set_is_connected(False)
                self.socket_offline = True
                print 'Connection to remote expired'
                self.close()

        while not self.socket_offline:
            try:
                if not self.socket_offline:
                    # Message received from server
                    self.heartbeat_server.recv(self.server_req_size)
            except socket.timeout, e:
                print e
                # if self.get_is_connected() and not self.socket_offline:
                print 'Connection to remote expired'
                self.close()
                self.socket_offline = True
                break

            if not self.socket_offline:
                # Message sent to server
                self.heartbeat_server.send(self.client_res_ms)

        self.heartbeat_server.close()

    def close(self, callback = None):
        if self.heartbeat_server.shutdown(0) == -1:
            print 'failure at shutdown heartbeat socket'
        self.heartbeat_server.close()
        self.socket_offline = True
        if callback is not None:
            callback()
