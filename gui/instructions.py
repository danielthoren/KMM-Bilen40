import json

class Instruction:
    """
    Instructions sent over tcp.
    """

    def __init__(self):
        self.W = False
        self.S = False
        self.A = False
        self.D = False
        self.start = False
        self.stop = False
        self.quit = False
        self.p = 0.0
        self.d = 0.0

    def encode(self):
        return (json.dumps(self.__dict__)).encode("ascii")

    def decode(self, msg):
        self.__dict__ = json.loads(msg.decode("ascii"))

    def reset_wasd(self):
        self.W = False
        self.S = False
        self.A = False
        self.D = False

    def printSelf(self):
        print("Forward:\t", self.W)
        print("Backward:\t", self.S)
        print("Left:\t\t", self.A)
        print("Right:\t\t", self.D)
        print("Start:\t\t", self.start)
        print("Stop:\t\t", self.stop)
        print("Quit:\t\t", self.quit)
        print("pid-P =\t", self.p)
        print("pid-D =\t", self.d)

    def _w(self, W):
        self.W = W

    def _s(self, S):
        self.S = S

    def _a(self, A):
        self.A = A

    def _d(self, D):
        self.D = D

    def doStart(self, start):
        self.start = start

    def doStop(self, stop):
        self.stop = stop

    def disconnect(self, quit):
        self.quit = quit

    def set_p(self, p):
        self.p = float(p)

    def set_d(self, d):
        self.d = float(d)
