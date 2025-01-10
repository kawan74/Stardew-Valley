from OpenGL.GL import *
from .colors import GREEN  # Agora a cor verde será importada corretamente

def draw_plant():
    # Desenha uma planta simples com cor verde
    glColor3fv(GREEN)  # Usando a cor verde
    plant_vertices = [
        [-0.05, -0.1],  # Parte inferior da planta
        [-0.05, 0.1],   # Parte superior
        [0.05, 0.1],    # Parte superior
        [0.05, -0.1]    # Parte inferior
    ]
    glBegin(GL_QUADS)
    for vertex in plant_vertices:
        glVertex2fv(vertex)
    glEnd()