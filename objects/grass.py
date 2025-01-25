from OpenGL.GL import *

def draw_grass():
    glColor3f(0.3, 0.7, 0.2)  # grama
    grass_vertices = [
        [-1, -1.3],  # Garantir que a grama fique no "chão"
        [-1.0, 0.2],
        [1.0, 0.2],
        [1.0, -1.3]
    ]
    glBegin(GL_QUADS)
    for vertex in grass_vertices:
        glVertex2fv(vertex)
    glEnd()