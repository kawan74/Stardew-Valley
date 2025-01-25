from OpenGL.GL import *  
from OpenGL.GLU import *  
import random

# Lista de posições das galinhas
pos_chickens = [
    [-0.5, 0.0, 0.0],
    [0.5, 0.2, 0.0],
]

def update_chickens():

    for i in range(len(pos_chickens)):

        dx = random.uniform(-0.02, 0.02)  # Movimento aleatório no eixo X
        dy = random.uniform(-0.02, 0.02)  # Movimento aleatório no eixo Y
        pos_chickens[i][0] += dx
        pos_chickens[i][1] += dy

        # Limita a posição das galinhas para dentro da tela
        pos_chickens[i][0] = max(min(pos_chickens[i][0], 1.0), -1.0)
        pos_chickens[i][1] = max(min(pos_chickens[i][1], 0.2), -1.3)

def draw_chicken():
    # Corpo da galinha (retângulo branco)
    glColor3f(1.0, 1.0, 1.0) 
    body_vertices = [
        [-0.2, -0.2],
        [-0.2, 0.2],
        [0.2, 0.2],
        [0.2, -0.2]
    ]
    glBegin(GL_QUADS)
    for vertex in body_vertices:
        glVertex2fv(vertex)
    glEnd()

    # Crista da galinha (retângulo vermelho)
    glColor3f(1.0, 0.0, 0.0) 
    crest_vertices = [
        [-0.05, 0.2],
        [-0.05, 0.3],
        [0.05, 0.3],
        [0.05, 0.2]
    ]
    glBegin(GL_QUADS)
    for vertex in crest_vertices:
        glVertex2fv(vertex)
    glEnd()

    # Bico da galinha (retângulo amarelo)
    glColor3f(1.0, 1.0, 0.0) 
    beak_vertices = [
        [0.1, -0.05],
        [0.1, 0.05],
        [0.2, 0.05],
        [0.2, -0.05]
    ]
    glBegin(GL_QUADS)
    for vertex in beak_vertices:
        glVertex2fv(vertex)
    glEnd()

def render_chickens():
    for pos in pos_chickens:
        glPushMatrix()  # Inicia uma nova transformação
        glTranslatef(pos[0], pos[1], pos[2])  # Move a galinha para a posição
        glScalef(0.2, 0.2, 1.0)  # Ajusta o tamanho da galinha
        draw_chicken()  # Desenha a galinha
        glPopMatrix()  # Restaura a transformação anterior
