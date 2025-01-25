from OpenGL.GL import *

def draw_house():
    # Casa
    glColor3f(0.9, 0.6, 0.3)  # Corpo da casa
    body_vertices = [
        [-0.3, -0.2],
        [-0.3, 0.2],
        [0.3, 0.2],
        [0.3, -0.2]
    ]
    glBegin(GL_QUADS)
    for vertex in body_vertices:
        glVertex2fv(vertex)
    glEnd()

    # Telhado
    glColor3f(0.7, 0.1, 0.1)
    roof_vertices = [
        [-0.4, 0.2],
        [0.4, 0.2],
        [0.0, 0.5]
    ]
    glBegin(GL_TRIANGLES)
    for vertex in roof_vertices:
        glVertex2fv(vertex)
    glEnd()

    # Porta
    glColor3f(0.5, 0.3, 0.1)  
    door_vertices = [
        [-0.05, -0.2],
        [-0.05, 0.05],
        [0.05, 0.05],
        [0.05, -0.2]
    ]
    glBegin(GL_QUADS)
    for vertex in door_vertices:
        glVertex2fv(vertex)
    glEnd()

    # Janela
    glColor3f(0.7, 0.9, 1.0)
    window_vertices = [
        [[-0.25, 0.0], [-0.15, 0.0], [-0.15, 0.1], [-0.25, 0.1]],
        [[0.15, 0.0], [0.25, 0.0], [0.25, 0.1], [0.15, 0.1]]
    ]
    for vertices in window_vertices:
        glBegin(GL_QUADS)
        for vertex in vertices:
            glVertex2fv(vertex)
        glEnd()