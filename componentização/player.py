import math
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

class Player:
    def __init__(self):
        self.pos = [0.0, 0.0, 0.0]
        self.rotation = [0.0, 0.0, 0.0]
        self.speed = 0.1

    def process_keyboard(self, window):
        front_x = math.cos(math.radians(self.rotation[1]))
        front_z = math.sin(math.radians(self.rotation[1]))

        nova_pos_x = self.pos[0]
        nova_pos_z = self.pos[2]

        if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
            nova_pos_x += self.speed * front_x
            nova_pos_z += self.speed * front_z
        if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
            nova_pos_x -= self.speed * front_x
            nova_pos_z -= self.speed * front_z
        if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
            nova_pos_x -= self.speed * front_z
            nova_pos_z += self.speed * front_x
        if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
            nova_pos_x += self.speed * front_z
            nova_pos_z -= self.speed * front_x

        limite_min, limite_max = -4.5, 4.5
        if limite_min <= nova_pos_x <= limite_max:
            self.pos[0] = nova_pos_x
        if limite_min <= nova_pos_z <= limite_max:
            self.pos[2] = nova_pos_z

    def draw(self):
        glPushMatrix()
        glTranslatef(self.pos[0], self.pos[1], self.pos[2])
        glRotatef(self.rotation[1] + 90, 0, 1, 0)
        
        # Corpo
        glColor3f(0.2, 0.4, 0.8)
        glPushMatrix()
        glScalef(0.2, 0.3, 0.1)
        quad = gluNewQuadric()
        gluCylinder(quad, 1, 1, 1, 16, 16)
        glPopMatrix()

        # Cabeça
        glColor3f(0.8, 0.6, 0.4)
        glPushMatrix()
        glTranslatef(0, 0.4, 0)
        quad = gluNewQuadric()
        gluSphere(quad, 0.1, 16, 16)
        glPopMatrix()

        # Braços
        glColor3f(0.2, 0.4, 0.8)
        for x in [-0.15, 0.15]:
            glPushMatrix()
            glTranslatef(x, 0.2, 0)
            glRotatef(90, 1, 0, 0)
            quad = gluNewQuadric()
            gluCylinder(quad, 0.03, 0.03, 0.2, 8, 8)
            glPopMatrix()

        # Pernas
        for x in [-0.07, 0.07]:
            glPushMatrix()
            glTranslatef(x, -0.1, 0)
            glRotatef(90, 1, 0, 0)
            quad = gluNewQuadric()
            gluCylinder(quad, 0.04, 0.04, 0.2, 8, 8)
            glPopMatrix()

        glPopMatrix()

    def move_forward(self):
        self.pos[2] -= self.speed

    def move_backward(self):
        self.pos[2] += self.speed

    def move_left(self):
        self.pos[0] -= self.speed

    def move_right(self):
        self.pos[0] += self.speed

    def rotate_left(self):
        self.rotation[1] -= 5.0

    def rotate_right(self):
        self.rotation[1] += 5.0