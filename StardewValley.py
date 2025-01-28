import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from math import sin, cos, radians
import random
from time import time

character_position = [0.0, -0.5]
movement_speed = 0.05

plant_positions = [[0.9 - i * 0.12, -0.8 + j *0.2] for i in range(5) for j in range(3)]

posChicken = [
    [-0.55, -0.35, 1],
    [-0.5, -0.5, 1],
    [-0.6, -0.55, 1],
    [-0.7, -0.4, 1],
    [-0.8, -0.7, 1]
]

directions = [[random.uniform(-0.005, 0.005), random.uniform(-0.005, 0.005)] for _ in posChicken]
last_update = time()

def setup_background():
    glClearColor(0.5, 0.8, 1.0, 1.0)  # céu

def draw_fence():
    # Postes verticais mais compridos e espaçados
    glColor3f(0.5, 0.3, 0.1)  # Cor marrom para os postes
    for i in range(-10, 11):  # Mais postes para torná-la mais comprida
        x = i * 0.1
        vertices = [
            [x - 0.01, -0.2],
            [x - 0.01, 0.1],
            [x + 0.01, 0.1],
            [x + 0.01, -0.2]
        ]
        glBegin(GL_QUADS)
        for vertex in vertices:
            glVertex2fv(vertex)
        glEnd()

    # Barras horizontais conectando os postes
    glColor3f(0.6, 0.4, 0.2)  # Cor mais clara para as barras
    for y_offset in [-0.05, 0.05]:  # Duas barras horizontais
        vertices = [
            [-1.0, y_offset - 0.01],  # Estende-se de -1.0 a 1.0
            [-1.0, y_offset + 0.01],
            [1.0, y_offset + 0.01],
            [1.0, y_offset - 0.01]
        ]
        glBegin(GL_QUADS)
        for vertex in vertices:
            glVertex2fv(vertex)
        glEnd()

def draw_house():
    glColor3f(0.9, 0.6, 0.3)  # casa
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

    # telhado
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

    # porta
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

    # janela
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

def draw_tree():
    # tronco da Ãrvore
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

    # copa da Ãrvore
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

def draw_chicken():
    # Corpo da galinha (retângulo branco)
    glColor3f(1.0, 1.0, 1.0)  # Branco
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
    glColor3f(1.0, 0.0, 0.0)  # Vermelho
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
    glColor3f(1.0, 1.0, 0.0)  # Amarelo
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

def update_chickens():
    global posChicken, directions, last_update

    # Limites do cercado
    min_x, max_x = -0.85, -0.35
    min_y, max_y = -0.85, -0.15

    # Atualizar posições das galinhas
    for i, pos in enumerate(posChicken):
        pos[0] += directions[i][0]
        pos[1] += directions[i][1]

        # Verificar colisões com os limites do cercado
        if pos[0] < min_x or pos[0] > max_x:
            directions[i][0] = -directions[i][0]  # Inverte a direção horizontal
            pos[0] = max(min(pos[0], max_x), min_x)  # Corrige a posição

        if pos[1] < min_y or pos[1] > max_y:
            directions[i][1] = -directions[i][1]  # Inverte a direção vertical
            pos[1] = max(min(pos[1], max_y), min_y)  # Corrige a posição

    # Troca direções aleatoriamente a cada 1 segundo
    if time() - last_update > 1:
        directions = [[random.uniform(-0.005, 0.005), random.uniform(-0.005, 0.005)] for _ in posChicken]
        last_update = time()

def draw_character():
    # Cabeça (marrom)
    glColor3f(0.6, 0.4, 0.2)
    glBegin(GL_QUADS)
    glVertex2f(-0.1, 0.2)
    glVertex2f(0.1, 0.2)
    glVertex2f(0.1, 0.4)
    glVertex2f(-0.1, 0.4)
    glEnd()

    # Olhos (brancos)
    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_QUADS)
    glVertex2f(-0.07, 0.3)
    glVertex2f(-0.03, 0.3)
    glVertex2f(-0.03, 0.35)
    glVertex2f(-0.07, 0.35)
    glEnd()

    glBegin(GL_QUADS)
    glVertex2f(0.03, 0.3)
    glVertex2f(0.07, 0.3)
    glVertex2f(0.07, 0.35)
    glVertex2f(0.03, 0.35)
    glEnd()

    # Cabelo (laranja)
    glColor3f(1.0, 0.5, 0.0)
    glBegin(GL_QUADS)
    glVertex2f(-0.1, 0.4)
    glVertex2f(0.1, 0.4)
    glVertex2f(0.1, 0.45)
    glVertex2f(-0.1, 0.45)
    glEnd()

    # Corpo (azul)
    glColor3f(0.0, 0.0, 1.0)
    glBegin(GL_QUADS)
    glVertex2f(-0.1, 0.0)
    glVertex2f(0.1, 0.0)
    glVertex2f(0.1, 0.2)
    glVertex2f(-0.1, 0.2)
    glEnd()

    # Pernas (cinza)
    glColor3f(0.8, 0.8, 0.8)
    glBegin(GL_QUADS)
    glVertex2f(-0.1, -0.2)
    glVertex2f(0.1, -0.2)
    glVertex2f(0.1, 0.0)
    glVertex2f(-0.1, 0.0)
    glEnd()

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



def render_scene():
    # Limpa a tela
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)      # modo de matriz: matriz de projeÃ§Ã£o
    glLoadIdentity()                 # carregando a matriz identidade
    glFrustum(-1, 1, -1, 1, 2, 100)  # definindo a matriz de projeÃ§Ã£o perspectiva
                                     # glFrustum(left, right, bottom, top, near, far)

    glMatrixMode(GL_MODELVIEW)     # modo de matriz: matriz de cÃ¢mera e de transformaÃ§Ã£o local
    glLoadIdentity()               # carregando matriz identidade
    gluLookAt(0,-1.5,3,   # definindo a posiÃ§Ã£o da cÃ¢mera
               0, 0, 0,   # definindo o alvo da cÃ¢mera (origem do sistema de coordenadas global)
               0, 1, 0)   # definindo a direÃ§Ã£o up da cÃ¢mera (direÃ§Ã£o do eixo y do sistema de coordenadas global)

    update_chickens()

    # Desenha a grama
    draw_grass()

    #Desenha as nuvens

    draw_cloud(-0.7, 0.7, 1.2)  # Nuvem maior
    draw_cloud(0.3, 0.6, 0.8)   # Nuvem menor
    draw_cloud(-0.1, 0.8, 1.0)  # Nuvem média

    # Desenha a cerca longa atrás da casa
    glPushMatrix()
    glTranslatef(0.0, 0.3, 0.0)  # Ajusta a posição da cerca atrás da casa
    draw_fence()
    glPopMatrix()

    # Translada a casa para cima e desenha
    glPushMatrix()
    glTranslatef(0.0, 0.2, 0.0)
    draw_house()
    glPopMatrix()
    

    # Desenha o cercado para os animais
    glPushMatrix()
    glTranslatef(-0.6, -0.5, 0.0)  # Posiciona o cercado na parte inferior do cenário
    glScale(0.7, 0.7, 1)
    draw_animal_fence()
    glPopMatrix()

    # Desenha árvores
    glPushMatrix()
    glTranslatef(-0.7, 0.0, 0.0)
    glScalef(0.6, 0.6, 1.0)
    draw_tree()
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.6, -0.1, 0.0)
    glScalef(0.6, 0.6, 1.0)
    draw_tree()
    glPopMatrix()

    for pos in posChicken:
        glPushMatrix()
        glTranslatef(pos[0], pos[1], pos[2])  # Posicione a galinha no cenário
        glScalef(0.2, 0.2, 1.0)        # Ajuste o tamanho da galinha
        draw_chicken()
        glPopMatrix()

    glPushMatrix()
    glTranslatef(character_position[0], character_position[1], 0.0)  # Usa a posição atualizada
    glScalef(0.5, 0.5, 1.0)
    draw_character()
    glPopMatrix()

    for i in plant_positions:
        glPushMatrix()
        glTranslatef(i[0], i[1], 0.0)  # Posiciona a planta
        glScalef(0.5, 0.5, 1)
        draw_plant()
        glPopMatrix()

def key_callback(window, key, scancode, action, mods):
    global character_position

    min_x, max_x = -1.0, 1.0
    min_y, max_y = -1.3, 0.2

    if action == glfw.PRESS or action == glfw.REPEAT:
        new_x, new_y = character_position[0], character_position[1]

        if key == glfw.KEY_W:  # Move para cima
            new_y += movement_speed
        elif key == glfw.KEY_S:  # Move para baixo
            new_y -= movement_speed
        elif key == glfw.KEY_A:  # Move para a esquerda
            new_x -= movement_speed
        elif key == glfw.KEY_D:  # Move para a direita
            new_x += movement_speed

        # Verifica se a nova posição está dentro dos limites
        if min_x <= new_x <= max_x and min_y <= new_y <= max_y:
            character_position[0], character_position[1] = new_x, new_y

def draw_cloud(x, y, scale=1.0):
    glPushMatrix()
    glTranslatef(x, y, 0)
    glScalef(scale, scale, 1.0)
    
    # Cor branca para a nuvem
    glColor3f(1.0, 1.0, 1.0)
    
    # Componentes da nuvem (círculos)
    positions = [
        (-0.2, 0.0), (0.0, 0.0), (0.2, 0.0),  # Parte inferior
        (-0.1, 0.1), (0.1, 0.1)               # Parte superior
    ]
    for cx, cy in positions:
        glPushMatrix()
        glTranslatef(cx, cy, 0)
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(0, 0)
        for angle in range(361):
            rad = radians(angle)
            glVertex2f(cos(rad) * 0.15, sin(rad) * 0.15)
        glEnd()
        glPopMatrix()
    
    glPopMatrix()


def main():
    if not glfw.init():
        return

    window = glfw.create_window(500, 500, "Stardew Valley", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)  # Registra o callback
    setup_background()

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render_scene()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()