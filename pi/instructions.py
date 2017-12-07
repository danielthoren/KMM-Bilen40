import json

class sendData:
    def __init__(self):
        self.lidar_data = [[0,0,0,0]]
        self.rpm = [0]
        self.lap = 0

        
    def encode(self):
        return (json.dumps(self.__dict__)).encode("ascii")

    def decode(self, msg):
        self.__dict__ = json.loads(msg.decode("ascii"))
        
class Instruction:
    """
    Instructions sent over tcp.
    """

    def __init__(self):
        self.W = False
        self.S = False
        self.AD = 0
        self.run = False
        self.auto_mode = False
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
        #self.AD = 0

    def _run(self):
        self.run = not self.run
        
    def printSelf(self):
        print("Forward:\t", self.W)
        print("Backward:\t", self.S)
        print("AD =\t\t", self.AD)
        print("Run:\t\t", self.run)
        print("Quit:\t\t", self.quit)
        print("pid-P =\t\t", self.p)
        print("pid-D =\t\t", self.d)
        print("Auto =\t\t", self.auto_mode)

        
    def _w(self):
        self.W = not self.W
        if self.S:
            self.S = False

    def _s(self):
        self.S = not self.S
        if self.W:
            self.W = False

    def _a(self):
        if self.AD > -1:
            self.AD -= 1

    def _d(self):
        if self.AD < 1:
            self.AD += 1
    def _auto_mode(self):
        self.auto_mode = not self.auto_mode

    def disconnect(self, quit):
        self.quit = quit

    def set_p(self, p):
        if not p:
            self.p = float(0)
        else:
            self.p = float(p)

    def set_d(self, d):
        if not d:
            self.d = float(0)
        else:
            self.d = float(d)
