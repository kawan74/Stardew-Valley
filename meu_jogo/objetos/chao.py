from OpenGL.GL import *
import math

def desenhar_chao():
    glColor3f(0.1, 0.7, 0.1)
    glBegin(GL_QUADS)
    glVertex3f(-5, -1, -5)
    glVertex3f(5, -1, -5)
    glVertex3f(5, -1, 5)
    glVertex3f(-5, -1, 5)
    glEnd() 