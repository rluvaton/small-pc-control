# Timer
from threading import Timer
import time


class HeartBeat(object):
    def __init__(self, message = 'HB',
                 response = 'T',
                 send_callback = None,
                 timeout = 5,
                 response_limit_timeout = 5,
                 response_limit_passed_callback = None,
                 sockets = None):
        # create the queue
        # create the sockets
        if sockets is None:
            sockets = []

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

        if sockets is None or len(sockets) == 0:
            sockets = []
            self.sockets = sockets
        else:
            self.sockets = sockets
            self.run_heartbeat = True
            self.run()

    def insert_socket(self, socket):
        """
        Insert new socket for the heartbeat technique
        :param socket: user socket
        """
        socket.settimeout(self.response_limit_timeout)

        self.sockets.append(socket)

        # If the first socket added then start the heartbeat technique
        if len(self.sockets) == 1:
            self.run_heartbeat = True
            self.run()

    def remove_socket(self, socket):
        """
        Remove socket from the heartbeat
        :param socket: Socket to remove
        """

        socket.settimeout(None)

        if socket in self.sockets:
            self.sockets.remove(socket)

        # If the last socket removed then stop the heartbeat technique
        if len(self.sockets) == 0:
            self.run_heartbeat = False

    def receive_every_seconds_method(self):
        for socket in self.sockets:
            try:
                response = socket.recv(self.response_bytes_size)
                if response == self.heartbeat_res:
                    print 'socket answered answer'
                else:
                    print 'socket didn\'t answer, response: {}'.format(response)
            except Exception, e:
                print 'Connection to remote expired'
                self.remove_socket(socket)

        # Here we put the received data into the queue
        # self.the_queue.put(self.receiving_socket.recv())

    def send_data_later(self):
        if not self.run_heartbeat:
            return

        for item in self.sockets:
            try:
                self.send_callback(item, self.heartbeat_ms)
            except Exception, e:
                print 'Error accrued, removing socket...'
                self.remove_socket(item)

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
