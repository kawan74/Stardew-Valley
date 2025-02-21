from OpenGL.GL import *
from OpenGL.GLU import *
import glfw
import time
import math
import random

from camera import Camera
from player import Player
from world import World
from entities import Entities

class JogoOpenGL:
    def __init__(self, largura=800, altura=800, titulo='Jogo'):
        self.largura = largura
        self.altura = altura
        self.titulo = titulo
        self.window = None
        
        self.player = Player()
        self.camera = Camera(self.player)
        self.world = World()
        self.entities = Entities()
        
        self.tempo_inicio = None
        self.first_mouse = True
        self.last_x = largura // 2
        self.last_y = altura // 2
        self.habilitar_movimento_mouse = True
        self.plantas = []  # Lista para armazenar as plantas

    def iniciar_janela(self):
        if not glfw.init():
            return False

        monitor = glfw.get_primary_monitor()
        video_mode = glfw.get_video_mode(monitor)

        self.window = glfw.create_window(video_mode.size.width, video_mode.size.height, self.titulo, monitor, None)
        if not self.window:
            glfw.terminate()
            return False

        glfw.make_context_current(self.window)
        glfw.set_cursor_pos_callback(self.window, self.mouse_callback)
        glfw.set_key_callback(self.window, self.teclado_callback)
        return True

    def mouse_callback(self, window, xpos, ypos):
        if not self.habilitar_movimento_mouse:
            return
        self.camera.process_mouse(xpos, ypos, self.first_mouse)
        if self.first_mouse:
            self.first_mouse = False

    def teclado_callback(self, window, key, scancode, action, mods):
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(self.window, True)
        if key == glfw.KEY_M and action == glfw.PRESS:
            self.habilitar_movimento_mouse = not self.habilitar_movimento_mouse

    def processar_entrada(self):
        self.player.process_keyboard(self.window)
        self.camera.update()

    def desenhar_cenario(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        tempo_decorrido = time.time() - self.tempo_inicio
        self.world.update_sky_color(tempo_decorrido)
        
        self.camera.apply()
        
        # Desenhar elementos do mundo
        self.world.draw()
        self.draw_player()
        self.entities.draw()

        # Desenhar todas as plantas
        for planta in self.plantas:
            if planta['tipo'] == 'tomate':
                self.draw_tomate(planta['x'], planta['z'])
            else:  # tipo == 'flor'
                self.draw_planta(planta['x'], planta['z'])

    def executar(self):
        if not self.iniciar_janela():
            return

        self.world.init_gl()
        self.tempo_inicio = time.time()

        while not glfw.window_should_close(self.window):
            glfw.poll_events()
            self.processar_entrada()
            self.entities.update()
            self.desenhar_cenario()
            glfw.swap_buffers(self.window)

        glfw.terminate()

    def adicionar_planta(self, tipo, x, z):
        """Adiciona uma nova planta ao jogo
        Args:
            tipo (str): Tipo da planta ('tomate' ou 'flor')
            x (float): Posição X da planta
            z (float): Posição Z da planta
        """
        self.plantas.append({
            'tipo': tipo,
            'x': x,
            'z': z
        })

    def draw_tomate(self, x, z):
        glPushMatrix()
        glTranslatef(x, -1, z)
        
        # Caule principal
        glColor3f(0.2, 0.5, 0.1)  # Verde escuro para o caule
        quad = gluNewQuadric()
        glPushMatrix()
        glRotatef(-90, 1, 0, 0)
        gluCylinder(quad, 0.03, 0.03, 0.5, 8, 1)
        glPopMatrix()
        
        # Folhas
        glColor3f(0.2, 0.6, 0.1)  # Verde para as folhas
        for angulo in [0, 45, 90, 135, 180, 225, 270, 315]:
            glPushMatrix()
            glTranslatef(0, 0.2, 0)
            glRotatef(angulo, 0, 1, 0)
            glRotatef(30, 1, 0, 0)
            glScalef(0.15, 0.05, 0.15)
            quad = gluNewQuadric()
            gluSphere(quad, 0.5, 8, 8)
            glPopMatrix()
        
        # Tomates vermelhos
        glColor3f(0.9, 0.1, 0.1)  # Vermelho vivo
        posicoes_tomates = [
            # Camada inferior
            (0.1, 0.15, 0.1),
            (-0.1, 0.15, -0.1),
            (0.15, 0.15, -0.05),
            (-0.15, 0.15, 0.1),
            
            # Camada média
            (0.1, 0.25, 0.0),
            (-0.05, 0.25, 0.15),
            (0.0, 0.25, -0.15),
            (-0.12, 0.25, 0.05),
            
            # Camada superior
            (0.08, 0.35, 0.08),
            (-0.08, 0.35, -0.08),
            (0.0, 0.35, 0.1),
            (-0.1, 0.35, 0.0),
            
            # Tomates no topo
            (0.05, 0.45, 0.0),
            (-0.05, 0.45, 0.05),
            (0.0, 0.45, -0.05)
        ]
        
        for pos in posicoes_tomates:
            glPushMatrix()
            glTranslatef(pos[0], pos[1], pos[2])
            tamanho = 0.07 + (abs(pos[0] * pos[2]) * 0.02)
            glScalef(tamanho, tamanho, tamanho)
            quad = gluNewQuadric()
            gluSphere(quad, 1.0, 8, 8)
            glPopMatrix()
            
            # Pequena folha verde no topo
            glColor3f(0.2, 0.5, 0.1)
            glPushMatrix()
            glTranslatef(pos[0], pos[1] + 0.04, pos[2])
            glScalef(0.02, 0.02, 0.02)
            gluSphere(quad, 1.0, 8, 8)
            glPopMatrix()
        
        glPopMatrix()

    def draw_planta(self, x, z):
        glPushMatrix()
        glTranslatef(x, -1, z)
        
        # Caule
        glColor3f(0.0, 0.5, 0.0)  # Verde para o caule
        quad = gluNewQuadric()
        glPushMatrix()
        glRotatef(-90, 1, 0, 0)
        gluCylinder(quad, 0.02, 0.02, 0.2, 8, 1)
        glPopMatrix()
        
        # Flores/Pétalas em roxo
        glColor3f(0.6, 0.0, 0.8)  # Roxo vibrante
        for angulo in [0, 72, 144, 216, 288]:  # 5 pétalas
            glPushMatrix()
            glTranslatef(0, 0.1, 0)
            glRotatef(angulo, 0, 1, 0)
            glRotatef(45, 1, 0, 0)
            glScalef(0.12, 0.12, 0.2)
            quad = gluNewQuadric()
            gluSphere(quad, 0.5, 8, 8)
            glPopMatrix()
        
        # Centro da flor em roxo mais escuro
        glColor3f(0.4, 0.0, 0.6)  # Roxo mais escuro
        glPushMatrix()
        glTranslatef(0, 0.1, 0)
        glScalef(0.1, 0.1, 0.1)
        gluSphere(quad, 0.5, 8, 8)
        glPopMatrix()
        
        glPopMatrix()

    def draw_player(self):
        glPushMatrix()
        try:
            glTranslatef(self.player.pos[0], self.player.pos[1] + 0.5, self.player.pos[2])  # Levantei um pouco o boneco
            glRotatef(self.player.rotation[1], 0, 1, 0)
            glScalef(1.5, 1.5, 1.5)  # Aumentei o tamanho geral do boneco
            
            quad = gluNewQuadric()
            
            # Corpo (tronco) - mais largo
            glColor3f(0.2, 0.4, 0.8)  # Azul mais vivo
            glPushMatrix()
            glScalef(0.4, 0.5, 0.3)
            gluCylinder(quad, 1.0, 0.8, 1.0, 16, 16)  # Usando cilindro para o corpo
            glPopMatrix()

            # Cabeça - maior e mais redonda
            glColor3f(0.95, 0.75, 0.6)  # Cor de pele
            glPushMatrix()
            glTranslatef(0, 0.8, 0)
            glScalef(0.4, 0.4, 0.4)
            gluSphere(quad, 1.0, 16, 16)
            glPopMatrix()

            # Cabelo - mais volumoso
            glColor3f(0.3, 0.2, 0.1)  # Castanho
            glPushMatrix()
            glTranslatef(0, 0.9, 0)
            glScalef(0.42, 0.2, 0.42)
            gluSphere(quad, 1.0, 16, 16)
            glPopMatrix()

            # Braços - mais grossos e curtos
            glColor3f(0.2, 0.4, 0.8)  # Azul
            # Braço esquerdo
            glPushMatrix()
            glTranslatef(-0.5, 0.3, 0)
            glRotatef(20, 0, 0, 1)
            glScalef(0.15, 0.4, 0.15)
            gluCylinder(quad, 1.0, 0.8, 1.0, 12, 12)
            glPopMatrix()
            
            # Braço direito
            glPushMatrix()
            glTranslatef(0.5, 0.3, 0)
            glRotatef(-20, 0, 0, 1)
            glScalef(0.15, 0.4, 0.15)
            gluCylinder(quad, 1.0, 0.8, 1.0, 12, 12)
            glPopMatrix()

            # Pernas - mais grossas
            glColor3f(0.2, 0.2, 0.7)  # Azul escuro
            # Perna esquerda
            glPushMatrix()
            glTranslatef(-0.2, -0.5, 0)
            glScalef(0.18, 0.5, 0.18)
            gluCylinder(quad, 1.0, 0.8, 1.0, 12, 12)
            glPopMatrix()
            
            # Perna direita
            glPushMatrix()
            glTranslatef(0.2, -0.5, 0)
            glScalef(0.18, 0.5, 0.18)
            gluCylinder(quad, 1.0, 0.8, 1.0, 12, 12)
            glPopMatrix()

        finally:
            glPopMatrix()
