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

        if self.main_socket is not None:
            self.user_actions = UserActions(lambda data: self.send(data, True))

        self.heartbeat_socket = heartbeat_socket

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

        if self.main_socket is not None:
            self.main_socket.close()

        if self.heartbeat_socket is not None:
            self.heartbeat_socket.close()

    def send(self, message, main = True):
        self.main_socket.send(message) if main else self.heartbeat_socket.send(message)

    def receive(self, size, main = True):
        return self.main_socket.recv(size) if main else self.heartbeat_socket.recv(size)
