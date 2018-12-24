# Timer
from threading import Timer
import time

# Singleton
singleton = None

class Exchange(object):
    def __init__(self):
        # create the queue
        # create the sockets
        pass

    def receive_every_seconds_method(self):
        # Here we put the received data into the queue
        self.the_queue.put(self.receiving_socket.recv())

    def send_data_later(self):
        while not self.the_queue.empty():
            self.emission_socket.send(self.the_queue.get())
        # reschedule
        self.schedule()

    def schedule(self, timeout = 30):
        self.timer = Timer(timeout, self.send_data_later)
        self.timer.start()

    def run(self):
        self.schedule(30)
        while self.continue_the_job:  # this is the stop condition
            self.receive_every_seconds_method()
            time.sleep(1)
