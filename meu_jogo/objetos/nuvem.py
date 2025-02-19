from OpenGL.GL import *
import math

def desenhar_nuvem(x, y, z=0):
    glColor3f(1, 1, 1)
    for deslocamento in [0, 0.2, -0.2]:
        glBegin(GL_TRIANGLE_FAN)
        for i in range(360):
            angulo = math.radians(i)
            glVertex3f(x + 0.2 * math.cos(angulo) + deslocamento, y + 0.2 * math.sin(angulo), z)
        glEnd()