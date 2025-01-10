from OpenGL.GL import *

def draw_plant():
    # Desenhar caule
    glColor3f(0.4, 0.25, 0.1)  # Marrom
    glBegin(GL_QUADS)
    for vertex in [[-0.02, 0.0], [0.02, 0.0], [0.02, 0.3], [-0.02, 0.3]]:
        glVertex2fv(vertex)
    glEnd()

    # Desenhar folhas (cor roxa)
    glColor3f(0.41, 0.24, 0.62)
    leaf_triangles = [
        [[-0.1, 0.2], [0.0, 0.25], [-0.1, 0.3]],  # Esquerda
        [[0.1, 0.2], [0.0, 0.25], [0.1, 0.3]],    # Direita
        [[-0.05, 0.3], [0.05, 0.3], [0.0, 0.4]],  # Topo
        [[-0.1, 0.1], [-0.02, 0.15], [-0.1, 0.2]],  # Esquerda inferior
        [[0.1, 0.1], [0.02, 0.15], [0.1, 0.2]],    # Direita inferior
        [[-0.1, 0.25], [-0.02, 0.3], [-0.1, 0.35]],  # Esquerda superior
        [[0.1, 0.25], [0.02, 0.3], [0.1, 0.35]]    # Direita superior
    ]
    for triangle in leaf_triangles:
        glBegin(GL_TRIANGLES)
        for vertex in triangle:
            glVertex2fv(vertex)
        glEnd()