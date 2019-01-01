from userActions import UserActions


# User Class for the user socket handling
class User(object):

    def __init__(self, socket, heartbeat_socket):
        """
        User Constructor
        :type socket: socket.socket or None
        :type heartbeat_socket: socket.socket
        :param socket: Main socket that made for requests
        :param heartbeat_socket: socket for the keep alive (heartbeat)
        """

        self.user_actions = None
        self.main_socket = socket
        self.open = True

        if self.main_socket is not None:
            self.user_actions = UserActions(lambda data: self.send(data, True))

        self.heartbeat_socket = heartbeat_socket

        self.main_socket_offline = False
        self.heartbeat_socket_offline = False

    def set_main_socket(self, socket):
        self.main_socket = socket

        if self.main_socket is not None:
            self.user_actions = UserActions(lambda data: self.send(data, True))

    def set_heartbeat_socket(self, socket):
        self.heartbeat_socket = socket

    def is_user_complete(self):
        return self.heartbeat_socket and self.main_socket

    def close(self):
        print 'Closing user'

        try:
            if self.main_socket is not None:
                if self.main_socket.shutdown(0) == -1:
                    print 'failure at shutdown user main socket'
                self.main_socket.close()
                self.main_socket_offline = True
        except Exception, err:
            self.main_socket_offline = True


        try:
            if self.heartbeat_socket is not None:
                if self.heartbeat_socket.shutdown(0) == -1:
                    print 'failure at shutdown user main socket'
                self.heartbeat_socket.close()
                self.heartbeat_socket_offline = True
        except Exception, err:
            self.heartbeat_socket_offline = True

    def send(self, message, main = True):
        self.main_socket.send(message) if main else self.heartbeat_socket.send(message)

    def receive(self, size, main = True):
        try:
            data = None
            if main:
                if self.main_socket_offline:
                    print 'Main Socket is shut show already'
                    return None
                data = self.main_socket.recv(size)
            else:
                if self.heartbeat_socket_offline:
                    print 'heartbeat Socket is shut show already'
                    return None
                data = self.heartbeat_socket.recv(size)
        except Exception, err:
            self.main_socket_offline = True
            self.heartbeat_socket_offline = True
            return None

        return data
