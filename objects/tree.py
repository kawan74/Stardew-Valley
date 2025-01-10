from OpenGL.GL import *
from math import sin, cos, radians

def draw_tree():
    # tronco da Árvore
    verticesTronco = [
        [-0.1, 0.0],
        [ 0.1, 0.0],
        [ 0.1, 0.4],
        [-0.1, 0.4],
    ]
    glColor3f(153/255,51/255,0/255)
    glBegin(GL_QUADS)
    for v in verticesTronco:
        glVertex2fv(v)
    glEnd()

    # copa da Árvore
    verticesCopa = []
    qtdDiv = 180
    deltaAng = 360/qtdDiv
    for div in range(qtdDiv):
        ang = div*deltaAng
        x = cos(radians(ang))
        y = sin(radians(ang))
        verticesCopa.append([x,y])
    
    glPushMatrix()
    glColor3f(0/255,100/255,0/255)
    glTranslatef(0.0,0.6,0.0)
    glScalef(0.36,0.36,1.0)
    glBegin(GL_TRIANGLE_FAN)
    for v in verticesCopa:
        glVertex2fv(v)
    glEnd()
    glPopMatrix()