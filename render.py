from OpenGL.GL import *  
from OpenGL.GLU import *  
from objects.grass import draw_grass
from objects.tree import draw_tree
from objects.fence import draw_animal_fence
from objects.house import draw_house
from objects.river import draw_river
from objects.character import draw_character
from objects.clouds import draw_cloud 
from objects.chicken import pos_chickens, draw_chicken, update_chickens 
from utils.colors import draw_plant 
from utils.drawing import draw_plant

character_position = [0.0, -0.4]
plant_positions = [
    [-0.4, -0.5],  # Planta 1
    [0.2, -0.6],   # Planta 2
    [0.5, -0.7],   # Planta 3
    [-0.2, -0.8],  # Planta 4
]

def render_scene():
    glClear(GL_COLOR_BUFFER_BIT)  # Limpa a tela

    # Atualiza as galinhas
    update_chickens()

    # Desenha a grama
    draw_grass()

    # Desenha as nuvens
    draw_cloud(-0.7, 0.7, 1.2)  # Nuvem maior
    draw_cloud(0.3, 0.6, 0.8)   # Nuvem menor
    draw_cloud(-0.1, 0.8, 1.0)  # Nuvem média

    # Desenha a cerca longa atrás da casa
    glPushMatrix()
    glTranslatef(0.0, 0.3, 0.0)  # Ajusta a posição da cerca atrás da casa
    draw_animal_fence()
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

    # Desenha as galinhas
    for pos in pos_chickens:  # Alterado para 'pos_chickens'
        glPushMatrix()
        glTranslatef(pos[0], pos[1], pos[2])  # Posiciona a galinha no cenário
        glScalef(0.2, 0.2, 1.0)  # Ajusta o tamanho da galinha
        draw_chicken()
        glPopMatrix()

    glPushMatrix()
    glTranslatef(character_position[0], character_position[1], 0.0)  # Usa a posição atualizada
    glScalef(0.5, 0.5, 1.0)
    draw_character() 
    glPopMatrix()

    # Desenha as plantas
    for i in plant_positions: 
        glPushMatrix()
        glTranslatef(i[0], i[1], 0.0)  # Posiciona a planta
        glScalef(0.5, 0.5, 1)
        draw_plant()
        glPopMatrix()
