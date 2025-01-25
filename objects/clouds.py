from OpenGL.GL import *
from math import cos, sin

def draw_cloud(x, y, size):
    glColor3f(1,1,1)
    glPushMatrix()
    glTranslatef(x, y, 0.0)  # Ajusta a posição da nuvem
    glScalef(size, size, 1.0)  # Ajusta o tamanho da nuvem

    glBegin(GL_POLYGON)
    for i in range(0, 360, 10):
        angle = i * 3.14159 / 180
        glVertex2f(0.5 * cos(angle), 0.5 * sin(angle))
    glEnd()

    glPopMatrix()