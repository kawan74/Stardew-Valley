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
from plantacao import adicionar_plantas

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
        
        self.tempo_inicio = time.time()
        self.first_mouse = True
        self.last_x = largura // 2
        self.last_y = altura // 2
        self.habilitar_movimento_mouse = True
        self.plantas = []
        self.monsters = []
        self.last_monster_spawn = 0
        self.monster_spawn_interval = 1
        self.dia_duracao = 20

        adicionar_plantas(self)  # Chama a função ao inicializar o jogo

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
        tempo_atual = time.time() - self.tempo_inicio
        horas = (tempo_atual % self.dia_duracao) * 24 / self.dia_duracao
        
        if horas >= 18 or horas < 6:
            glClearColor(0.1, 0.1, 0.3, 1.0)
            self.spawn_monster()
        else:
            glClearColor(0.5, 0.7, 1.0, 1.0)
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        tempo_decorrido = time.time() - self.tempo_inicio
        self.world.update_sky_color(tempo_decorrido)
        
        self.camera.apply()
        
        self.world.draw()
        self.player.draw()
        self.entities.draw()

        for planta in self.plantas:
            if planta['tipo'] == 'tomate':
                self.draw_tomate(planta['x'], planta['z'])
            else:
                self.draw_planta(planta['x'], planta['z'])

        for monster in self.monsters:
            self.draw_monster(monster['x'], monster['y'], monster['z'])
            self.update_monster_position(monster)

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
        self.plantas.append({
            'tipo': tipo,
            'x': x,
            'z': z
        })

    def draw_tomate(self, x, z):
        glPushMatrix()
        glTranslatef(x, -1, z)
        
        glColor3f(0.2, 0.5, 0.1)
        quad = gluNewQuadric()
        glPushMatrix()
        glRotatef(-90, 1, 0, 0)
        gluCylinder(quad, 0.03, 0.03, 0.5, 8, 1)
        glPopMatrix()
        
        glColor3f(0.2, 0.6, 0.1)
        for angulo in [0, 45, 90, 135, 180, 225, 270, 315]:
            glPushMatrix()
            glTranslatef(0, 0.2, 0)
            glRotatef(angulo, 0, 1, 0)
            glRotatef(30, 1, 0, 0)
            glScalef(0.15, 0.05, 0.15)
            quad = gluNewQuadric()
            gluSphere(quad, 0.5, 8, 8)
            glPopMatrix()
        
        glColor3f(0.9, 0.1, 0.1)
        posicoes_tomates = [
            (0.1, 0.15, 0.1),
            (-0.1, 0.15, -0.1),
            (0.15, 0.15, -0.05),
            (-0.15, 0.15, 0.1),
            (0.1, 0.25, 0.0),
            (-0.05, 0.25, 0.15),
            (0.0, 0.25, -0.15),
            (-0.12, 0.25, 0.05),
            (0.08, 0.35, 0.08),
            (-0.08, 0.35, -0.08),
            (0.0, 0.35, 0.1),
            (-0.1, 0.35, 0.0),
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
            
            glColor3f(0.2, 0.5, 0.1)
            glPushMatrix()
            glTranslatef(pos[0], pos[1] + 0.04, pos[2])
            glScalef(0.02, 0.02, 0.02)
            gluSphere(quad, 1.0, 8, 8)
            glPopMatrix()
        
        glPopMatrix()

    def draw_planta(self, x, z):
        glPushMatrix()
        glTranslatef(x + 0.5, -1, z)
        
        glColor3f(0.0, 0.5, 0.0)
        quad = gluNewQuadric()
        glPushMatrix()
        glRotatef(-90, 1, 0, 0)
        gluCylinder(quad, 0.02, 0.02, 0.2, 8, 1)
        glPopMatrix()
        
        glColor3f(0.6, 0.0, 0.8)
        for angulo in [0, 72, 144, 216, 288]:
            glPushMatrix()
            glTranslatef(0, 0.1, 0)
            glRotatef(angulo, 0, 1, 0)
            glRotatef(45, 1, 0, 0)
            glScalef(0.12, 0.12, 0.2)
            quad = gluNewQuadric()
            gluSphere(quad, 0.5, 8, 8)
            glPopMatrix()
        
        glColor3f(0.4, 0.0, 0.6)
        glPushMatrix()
        glTranslatef(0, 0.1, 0)
        glScalef(0.1, 0.1, 0.1)
        gluSphere(quad, 0.5, 8, 8)
        glPopMatrix()
        
        glPopMatrix()

    def draw_player(self):
        glPushMatrix()
        try:
            glTranslatef(self.player.pos[0], self.player.pos[1] + 0.5, self.player.pos[2])
            glRotatef(self.player.rotation[1], 0, 1, 0)
            glScalef(1.5, 1.5, 1.5)
            
            quad = gluNewQuadric()
            
            glColor3f(0.2, 0.4, 0.8)
            glPushMatrix()
            glScalef(0.4, 0.5, 0.3)
            gluCylinder(quad, 1.0, 0.8, 1.0, 16, 16)
            glPopMatrix()

            glColor3f(0.95, 0.75, 0.6)
            glPushMatrix()
            glTranslatef(0, 0.8, 0)
            glScalef(0.4, 0.4, 0.4)
            gluSphere(quad, 1.0, 16, 16)
            glPopMatrix()

            glColor3f(0.3, 0.2, 0.1)
            glPushMatrix()
            glTranslatef(0, 0.9, 0)
            glScalef(0.42, 0.2, 0.42)
            gluSphere(quad, 1.0, 16, 16)
            glPopMatrix()

            glColor3f(0.2, 0.4, 0.8)
            glPushMatrix()
            glTranslatef(-0.5, 0.3, 0)
            glRotatef(20, 0, 0, 1)
            glScalef(0.15, 0.4, 0.15)
            gluCylinder(quad, 1.0, 0.8, 1.0, 12, 12)
            glPopMatrix()
            
            glPushMatrix()
            glTranslatef(0.5, 0.3, 0)
            glRotatef(-20, 0, 0, 1)
            glScalef(0.15, 0.4, 0.15)
            gluCylinder(quad, 1.0, 0.8, 1.0, 12, 12)
            glPopMatrix()

            glColor3f(0.2, 0.2, 0.7)
            glPushMatrix()
            glTranslatef(-0.2, -0.5, 0)
            glScalef(0.18, 0.5, 0.18)
            gluCylinder(quad, 1.0, 0.8, 1.0, 12, 12)
            glPopMatrix()
            
            glPushMatrix()
            glTranslatef(0.2, -0.5, 0)
            glScalef(0.18, 0.5, 0.18)
            gluCylinder(quad, 1.0, 0.8, 1.0, 12, 12)
            glPopMatrix()

        finally:
            glPopMatrix()

    def spawn_monster(self):
        tempo_atual = time.time() - self.tempo_inicio
        
        if tempo_atual - self.last_monster_spawn > self.monster_spawn_interval:
            angulo = random.uniform(0, 2 * math.pi)
            distancia = 8
            
            x = self.player.pos[0] + distancia * math.cos(angulo)
            z = self.player.pos[2] + distancia * math.sin(angulo)
            
            novo_monstro = {
                'x': x,
                'y': 0,
                'z': z,
                'speed': 0.1
            }
            
            self.monsters.append(novo_monstro)
            self.last_monster_spawn = tempo_atual

    def update_monster_position(self, monster):
        dx = self.player.pos[0] - monster['x']
        dz = self.player.pos[2] - monster['z']
        distancia = math.sqrt(dx*dx + dz*dz)
        
        if distancia > 0.5:
            monster['x'] += (dx/distancia) * monster['speed']
            monster['z'] += (dz/distancia) * monster['speed']
        
        if distancia < 1.0:
            self.monsters.remove(monster)

    def draw_monster(self, x, y, z):
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

        light_pos = [1.0, 1.0, 1.0, 1.0]
        glLightfv(GL_LIGHT0, GL_POSITION, light_pos)

        spot_direction = [-1.0, -1.0, -1.0]
        glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, spot_direction)

        glLightf(GL_LIGHT0, GL_SPOT_CUTOFF, 90.0)

        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.02, 0.02, 0.02, 1.0])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.1, 0.1, 0.1, 1.0])
        glLightfv(GL_LIGHT0, GL_SPECULAR, [0.2, 0.2, 0.2, 1.0])

        glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 1.0)
        glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.1)
        glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0.05)

        glMaterialfv(GL_FRONT, GL_AMBIENT, [0.02, 0.02, 0.02, 1.0])
        glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.1, 0.1, 0.1, 1.0])
        glMaterialfv(GL_FRONT, GL_SPECULAR, [0.1, 0.1, 0.1, 1.0])
        glMaterialf(GL_FRONT, GL_SHININESS, 8.0)

        glPushMatrix()
        glTranslatef(x, y, z)
        glScalef(0.1, 0.1, 0.1)

        quad = gluNewQuadric()

        glColor3f(0.1, 0.1, 0.1)
        glPushMatrix()
        glScalef(1.0, 1.2, 0.8)
        gluSphere(quad, 1.0, 16, 16)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(0, 1.0, 0)
        glScalef(0.8, 0.8, 0.8)
        gluSphere(quad, 1.0, 16, 16)

        for lado in [-0.3, 0.3]:
            glPushMatrix()
            glTranslatef(lado, 0.2, 0.7)

            glColor3f(0.9, 0.9, 0.9)
            gluSphere(quad, 0.25, 12, 12)

            glColor3f(1.0, 0.0, 0.0)
            glTranslatef(0, 0, 0.15)
            gluSphere(quad, 0.15, 8, 8)

            glColor3f(0.0, 0.0, 0.0)
            glTranslatef(0, 0, 0.05)
            gluSphere(quad, 0.08, 8, 8)

            glPopMatrix()

        glColor3f(0.95, 0.95, 0.95)
        for lado in [-0.2, 0.2]:
            glPushMatrix()
            glTranslatef(lado, -0.2, 0.7)
            glRotatef(45, 1, 0, 0)
            gluCylinder(quad, 0.08, 0.0, 0.3, 8, 1)
            glPopMatrix()

        glPopMatrix()

        glColor3f(0.15, 0.15, 0.15)
        for lado in [-1, 1]:
            glPushMatrix()
            glTranslatef(lado * 0.8, 0.3, 0)

            gluSphere(quad, 0.3, 12, 12)

            glRotatef(lado * 20, 0, 0, 1)
            glRotatef(30, 1, 0, 0)
            gluCylinder(quad, 0.2, 0.15, 0.8, 12, 1)

            glTranslatef(0, 0, 0.8)
            gluSphere(quad, 0.2, 12, 12)

            glRotatef(30, 1, 0, 0)
            gluCylinder(quad, 0.15, 0.1, 0.6, 12, 1)

            glTranslatef(0, 0, 0.6)
            gluSphere(quad, 0.2, 12, 12)

            glPopMatrix()

        for lado in [-1, 1]:
            glPushMatrix()
            glTranslatef(lado * 0.4, -1.0, 0)

            glColor3f(0.15, 0.15, 0.15)
            glRotatef(lado * 10, 0, 0, 1)
            gluCylinder(quad, 0.25, 0.2, 0.8, 12, 1)

            glTranslatef(0, 0, 0.8)
            gluSphere(quad, 0.25, 12, 12)

            glRotatef(10, 1, 0, 0)
            gluCylinder(quad, 0.2, 0.15, 0.7, 12, 1)

            glTranslatef(0, 0, 0.7)
            glScalef(1.0, 1.0, 1.5)
            gluSphere(quad, 0.2, 12, 12)

            glPopMatrix()

        glColor3f(0.05, 0.05, 0.05)
        for pos in [(0.5, 0.5, 0.3), (-0.5, 0.3, 0.4), (0.3, -0.4, 0.5), (-0.4, -0.2, 0.3)]:
            glPushMatrix()
            glTranslatef(*pos)
            glScalef(0.2, 0.2, 0.1)
            gluSphere(quad, 1.0, 8, 8)
            glPopMatrix()

        glPopMatrix()
        glDisable(GL_LIGHTING)