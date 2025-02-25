import math
import glfw
from OpenGL.GLU import *

class Camera:
    def __init__(self, player):
        self.player = player
        self.pos = [0, 0, 3]
        self.yaw = -90.0
        self.pitch = 0.0
        self.sensibilidade = 0.1
        self.distance = 3.0
        self.height = 1.5
        self.last_x = None
        self.last_y = None

    def process_mouse(self, xpos, ypos, first_mouse):
        if first_mouse:
            self.last_x = xpos
            self.last_y = ypos
            return

        xoffset = (xpos - self.last_x) * self.sensibilidade
        yoffset = (self.last_y - ypos) * self.sensibilidade

        self.last_x = xpos
        self.last_y = ypos

        self.yaw += xoffset
        self.pitch += yoffset
        self.pitch = max(-89.0, min(89.0, self.pitch))

    def update(self):
        camera_offset_x = -self.distance * math.cos(math.radians(self.yaw)) * math.cos(math.radians(self.pitch))
        camera_offset_y = -self.distance * math.sin(math.radians(self.pitch))
        camera_offset_z = -self.distance * math.sin(math.radians(self.yaw)) * math.cos(math.radians(self.pitch))

        self.pos[0] = self.player.pos[0] + camera_offset_x
        self.pos[1] = self.player.pos[1] + camera_offset_y + self.height
        self.pos[2] = self.player.pos[2] + camera_offset_z

    def apply(self):
        gluLookAt(
            self.pos[0], self.pos[1], self.pos[2],
            self.player.pos[0], self.player.pos[1] + 1, self.player.pos[2],
            0, 1, 0
        )