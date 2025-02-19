import math

class Camera:
    def __init__(self):
        self.pos = [0, 0, -3]
        self.yaw = -90.0
        self.pitch = 0.0
        self.sensibilidade = 0.1
