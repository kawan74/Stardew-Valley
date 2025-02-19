from OpenGL.GL import *
import math

def desenhar_casa():
    glColor3f(0.8, 0.5, 0.2)
    glBegin(GL_QUADS)
    glVertex3f(-0.3, -1, 0.0)
    glVertex3f(-0.3, -0.6, 0.0)
    glVertex3f(0.3, -0.6, 0.0)
    glVertex3f(0.3, -1, 0.0)
    glEnd()

    glColor3f(0.5, 0.2, 0.1)
    glBegin(GL_TRIANGLES)
    glVertex3f(-0.35, -0.6, 0.0)
    glVertex3f(0.35, -0.6, 0.0)
    glVertex3f(0.0, -0.3, 0.0)
    glEnd()