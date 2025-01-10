from OpenGL.GL import *

def draw_animal_fence():
    # Postes nos cantos
    glColor3f(0.5, 0.3, 0.1)  # Cor marrom para os postes
    corner_positions = [
        [-0.5, -0.5],
        [-0.5, 0.5],
        [0.5, 0.5],
        [0.5, -0.5]
    ]
    for x, y in corner_positions:
        vertices = [
            [x - 0.02, y - 0.02],
            [x - 0.02, y + 0.02],
            [x + 0.02, y + 0.02],
            [x + 0.02, y - 0.02],
        ]
        glBegin(GL_QUADS)
        for vertex in vertices:
            glVertex2fv(vertex)
        glEnd()

    # Barras horizontais (superior e inferior)
    glColor3f(0.6, 0.4, 0.2)  # Cor mais clara para as barras
    horizontal_positions = [-0.5, 0.5]
    for y in horizontal_positions:
        vertices = [
            [-0.5, y - 0.01],
            [-0.5, y + 0.01],
            [0.5, y + 0.01],
            [0.5, y - 0.01]
        ]
        glBegin(GL_QUADS)
        for vertex in vertices:
            glVertex2fv(vertex)
        glEnd()

    # Barras verticais (esquerda e direita)
    vertical_positions = [-0.5, 0.5]
    for x in vertical_positions:
        vertices = [
            [x - 0.01, -0.5],
            [x + 0.01, -0.5],
            [x + 0.01, 0.5],
            [x - 0.01, 0.5]
        ]
        glBegin(GL_QUADS)
        for vertex in vertices:
            glVertex2fv(vertex)
        glEnd()