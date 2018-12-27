# Timer
from threading import Timer
import time

from user import User


# Heartbeat
class HeartBeat(object):
    users = None  # type: List[User]

    def __init__(self, message = 'HB',
                 response = 'T',
                 send_callback = None,
                 timeout = 5,
                 response_limit_timeout = 5,
                 response_limit_passed_callback = None,
                 users = None):
        if users is None:
            users = []

        if response_limit_passed_callback is None:
            def response_limit_passed_callback(client):
                pass

        if send_callback is None:
            def send_callback(client, mess):
                pass

        self.timeout = timeout

        self.response_limit_timeout = response_limit_timeout
        self.response_limit_passed_callback = response_limit_passed_callback

        self.heartbeat_ms = message
        self.heartbeat_res = response

        self.response_bytes_size = len(response.encode('utf-8'))

        self.run_heartbeat = False

        self.send_callback = send_callback

        # Declare the timer
        self.timer = None

        if users is None or len(users) == 0:
            users = []
            self.users = users
        else:
            self.users = users
            self.run_heartbeat = True
            self.run()

    def add(self, user):
        """
        Insert new socket for the heartbeat technique
        :type user: User
        :param user: User
        """
        user.heartbeat_socket.settimeout(self.response_limit_timeout)

        self.users.append(user)

        # If the first socket added then start the heartbeat technique
        if len(self.users) == 1:
            self.run_heartbeat = True
            self.run()

    def remove(self, user):
        """
        Remove socket from the heartbeat
        :type user: User
        :param user: Socket to remove
        """

        user.heartbeat_socket.settimeout(None)

        if user in self.users:
            self.users.remove(user)

        # If the last socket removed then stop the heartbeat technique
        if len(self.users) == 0:
            self.run_heartbeat = False

    def receive_every_seconds_method(self):
        for user in self.users:  # type: User
            try:
                user.receive(self.response_bytes_size, False)
            except Exception, e:
                self.response_limit_passed_callback(user)
                self.remove(user)

        # Here we put the received data into the queue
        # self.the_queue.put(self.receiving_socket.recv())

    def send_data_later(self):
        if not self.run_heartbeat:
            return

        for user in self.users:
            try:
                self.send_callback(user, self.heartbeat_ms)
            except Exception, e:
                print 'Error accrued, removing socket...'
                self.remove(user)

        # while not self.the_queue.empty():
        #     self.emission_socket.send(self.the_queue.get())

        # reschedule
        self.schedule()

    def schedule(self):
        self.timer = Timer(self.timeout, self.send_data_later)
        self.timer.start()

    def run(self):
        self.schedule()
        while self.run_heartbeat:  # this is the stop condition
            self.receive_every_seconds_method()
            time.sleep(self.timeout)
