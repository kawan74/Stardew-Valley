from OpenGL.GL import *
from math import radians, cos, sin

def draw_character():
    # Corpo do personagem (quadrado azul)
    glColor3f(0.0, 0.0, 1.0)  # Cor azul
    body_vertices = [
        [-0.1, -0.1],
        [-0.1, 0.1],
        [0.1, 0.1],
        [0.1, -0.1]
    ]
    glBegin(GL_QUADS)
    for vertex in body_vertices:
        glVertex2fv(vertex)
    glEnd()

    # Cabeça do personagem (círculo amarelo)
    glColor3f(1.0, 1.0, 0.0)  # Cor amarela
    glPushMatrix()
    glTranslatef(0.0, 0.15, 0.0)  # Translada a cabeça para cima
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(0, 0)  # Centro da cabeça
    for angle in range(361):
        rad = radians(angle)
        glVertex2f(cos(rad) * 0.1, sin(rad) * 0.1)  # Desenha o círculo
    glEnd()
    glPopMatrix()
