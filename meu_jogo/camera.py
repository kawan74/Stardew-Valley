from OpenGL.GL import *
from OpenGL.GLU import *
import math
import glfw

class Camera:
    def __init__(self):
        self.pos = [0.0, 0.0, 3.0]  # Posição inicial da câmera
        self.front = [0.0, 0.0, -1.0]  # Direção para onde a câmera olha (eixo Z negativo)
        self.up = [0.0, 1.0, 0.0]  # Direção "para cima" da câmera (eixo Y)
        self.right = [1.0, 0.0, 0.0]  # Direção para a direita da câmera (eixo X)
        
        self.yaw = -90.0  # Ângulo inicial em torno do eixo Y
        self.pitch = 0.0  # Ângulo inicial em torno do eixo X
        self.sensibilidade = 0.1

    def update(self, delta_time):
        """Atualiza a direção da câmera com base nos inputs do teclado e mouse"""
        if glfw.get_key(self.window, glfw.KEY_W) == glfw.PRESS:
            self.pos = [self.pos[i] + self.front[i] * delta_time for i in range(3)]
        if glfw.get_key(self.window, glfw.KEY_S) == glfw.PRESS:
            self.pos = [self.pos[i] - self.front[i] * delta_time for i in range(3)]
        if glfw.get_key(self.window, glfw.KEY_A) == glfw.PRESS:
            self.pos = [self.pos[i] - self.right[i] * delta_time for i in range(3)]
        if glfw.get_key(self.window, glfw.KEY_D) == glfw.PRESS:
            self.pos = [self.pos[i] + self.right[i] * delta_time for i in range(3)]

    def process_mouse_movement(self, x_offset, y_offset):
        """Atualiza a direção da câmera com base no movimento do mouse"""
        x_offset *= self.sensibilidade
        y_offset *= self.sensibilidade

        self.yaw += x_offset
        self.pitch -= y_offset  # Inverter o movimento do mouse para corrigir a rotação
        self.pitch = max(-89.0, min(89.0, self.pitch))  # Limitar o pitch para não virar de cabeça para baixo

        self.update_camera_vectors()

    def update_camera_vectors(self):
        """Atualiza a direção da câmera com base nos ângulos de yaw e pitch"""
        rad_yaw = math.radians(self.yaw)
        rad_pitch = math.radians(self.pitch)

        self.front[0] = math.cos(rad_yaw) * math.cos(rad_pitch)
        self.front[1] = math.sin(rad_pitch)
        self.front[2] = math.sin(rad_yaw) * math.cos(rad_pitch)

        self.right = self.normalize(self.cross_product(self.front, self.up))  # Direção à direita
        self.up = self.normalize(self.cross_product(self.right, self.front))  # Direção "para cima"

    def normalize(self, vec):
        """Normaliza o vetor"""
        length = math.sqrt(sum([x ** 2 for x in vec]))
        return [x / length for x in vec]

    def cross_product(self, v1, v2):
        """Produto vetorial entre dois vetores"""
        return [v1[1] * v2[2] - v1[2] * v2[1], 
                v1[2] * v2[0] - v1[0] * v2[2], 
                v1[0] * v2[1] - v1[1] * v2[0]]
