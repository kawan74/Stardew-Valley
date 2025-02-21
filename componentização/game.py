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
        
        self.tempo_inicio = time.time()
        self.first_mouse = True
        self.last_x = largura // 2
        self.last_y = altura // 2
        self.habilitar_movimento_mouse = True
        self.plantas = []  # Lista para armazenar as plantas
        self.monsters = []
        self.last_monster_spawn = 0
        self.monster_spawn_interval = 1  # Spawn mais frequente
        self.dia_duracao = 20  # 20 segundos por dia (10 dia + 10 noite)

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
        
        # Debug da hora
        print(f"Hora atual: {horas:.1f}, Monstros: {len(self.monsters)}")
        
        # Definir se é dia ou noite
        if horas >= 18 or horas < 6:  # Noite
            glClearColor(0.1, 0.1, 0.3, 1.0)  # Céu escuro
            self.spawn_monster()  # Tenta criar monstro
        else:  # Dia
            glClearColor(0.5, 0.7, 1.0, 1.0)  # Céu claro
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        tempo_decorrido = time.time() - self.tempo_inicio
        self.world.update_sky_color(tempo_decorrido)
        
        self.camera.apply()
        
        # Desenhar elementos do mundo
        self.world.draw()
        self.player.draw()
        self.entities.draw()

        # Desenhar todas as plantas
        for planta in self.plantas:
            if planta['tipo'] == 'tomate':
                self.draw_tomate(planta['x'], planta['z'])
            else:  # tipo == 'flor'
                self.draw_planta(planta['x'], planta['z'])

        # Desenhar monstros
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

    def spawn_monster(self):
        tempo_atual = time.time() - self.tempo_inicio
        
        if tempo_atual - self.last_monster_spawn > self.monster_spawn_interval:
            # Posição aleatória em volta do jogador
            angulo = random.uniform(0, 2 * math.pi)
            distancia = 8  # Distância fixa do jogador
            
            x = self.player.pos[0] + distancia * math.cos(angulo)
            z = self.player.pos[2] + distancia * math.sin(angulo)
            
            novo_monstro = {
                'x': x,
                'y': 0,
                'z': z,
                'speed': 0.1  # Velocidade aumentada
            }
            
            self.monsters.append(novo_monstro)
            self.last_monster_spawn = tempo_atual
            print(f"Monstro criado em ({x:.1f}, {z:.1f})")

    def update_monster_position(self, monster):
        # Mover em direção ao jogador
        dx = self.player.pos[0] - monster['x']
        dz = self.player.pos[2] - monster['z']
        distancia = math.sqrt(dx*dx + dz*dz)
        
        if distancia > 0.3:  # Se não está muito perto
            monster['x'] += (dx/distancia) * monster['speed']
            monster['z'] += (dz/distancia) * monster['speed']
        
        # Remover monstro se encostar no jogador
        if distancia < 0.5:
            self.monsters.remove(monster)
            print("Monstro removido")

    def draw_monster(self, x, y, z):
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

        # Definir a posição da luz
        light_pos = [1.0, 1.0, 1.0, 1.0]
        glLightfv(GL_LIGHT0, GL_POSITION, light_pos)

        # Definir a direção da luz spot
        spot_direction = [-1.0, -1.0, -1.0]  # Direção para onde a luz está apontando
        glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, spot_direction)

        # Definir o ângulo de corte da luz spot
        glLightf(GL_LIGHT0, GL_SPOT_CUTOFF, 90.0)  # Ângulo de corte em graus

        # Diminuir ainda mais as propriedades da luz
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.02, 0.02, 0.02, 1.0])  # Muito reduzido
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.1, 0.1, 0.1, 1.0])    # Muito reduzido
        glLightfv(GL_LIGHT0, GL_SPECULAR, [0.2, 0.2, 0.2, 1.0])   # Muito reduzido

        # Configurar atenuação da luz
        glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 1.0)
        glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.1)
        glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0.05)

        # Diminuir ainda mais as propriedades do material do monstro
        glMaterialfv(GL_FRONT, GL_AMBIENT, [0.02, 0.02, 0.02, 1.0])  # Muito reduzido
        glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.1, 0.1, 0.1, 1.0])     # Muito reduzido
        glMaterialfv(GL_FRONT, GL_SPECULAR, [0.1, 0.1, 0.1, 1.0])    # Muito reduzido
        glMaterialf(GL_FRONT, GL_SHININESS, 8.0)                     # Muito reduzido

        glPushMatrix()
        glTranslatef(x, y, z)
        glScalef(0.1, 0.1, 0.1)  # Tamanho base do monstro

        quad = gluNewQuadric()

        # Corpo principal (torso)
        glColor3f(0.1, 0.1, 0.1)  # Preto principal
        glPushMatrix()
        glScalef(1.0, 1.2, 0.8)
        gluSphere(quad, 1.0, 16, 16)
        glPopMatrix()

        # Cabeça
        glPushMatrix()
        glTranslatef(0, 1.0, 0)
        glScalef(0.8, 0.8, 0.8)
        gluSphere(quad, 1.0, 16, 16)

        # Olhos (brilhantes em contraste com o corpo preto)
        for lado in [-0.3, 0.3]:
            glPushMatrix()
            glTranslatef(lado, 0.2, 0.7)

            # Globo ocular (branco)
            glColor3f(0.9, 0.9, 0.9)
            gluSphere(quad, 0.25, 12, 12)

            # Íris (vermelho intenso)
            glColor3f(1.0, 0.0, 0.0)
            glTranslatef(0, 0, 0.15)
            gluSphere(quad, 0.15, 8, 8)

            # Pupila (preta)
            glColor3f(0.0, 0.0, 0.0)
            glTranslatef(0, 0, 0.05)
            gluSphere(quad, 0.08, 8, 8)

            glPopMatrix()

        # Presas (branco marfim)
        glColor3f(0.95, 0.95, 0.95)
        for lado in [-0.2, 0.2]:
            glPushMatrix()
            glTranslatef(lado, -0.2, 0.7)
            glRotatef(45, 1, 0, 0)
            gluCylinder(quad, 0.08, 0.0, 0.3, 8, 1)
            glPopMatrix()

        glPopMatrix()  # Fim da cabeça

        # Braços
        glColor3f(0.15, 0.15, 0.15)  # Preto um pouco mais claro para contraste
        for lado in [-1, 1]:
            glPushMatrix()
            glTranslatef(lado * 0.8, 0.3, 0)

            # Ombro
            gluSphere(quad, 0.3, 12, 12)

            # Braço superior
            glRotatef(lado * 20, 0, 0, 1)
            glRotatef(30, 1, 0, 0)
            gluCylinder(quad, 0.2, 0.15, 0.8, 12, 1)

            # Cotovelo
            glTranslatef(0, 0, 0.8)
            gluSphere(quad, 0.2, 12, 12)

            # Antebraço
            glRotatef(30, 1, 0, 0)
            gluCylinder(quad, 0.15, 0.1, 0.6, 12, 1)

            # Mão
            glTranslatef(0, 0, 0.6)
            gluSphere(quad, 0.2, 12, 12)

            glPopMatrix()

        # Pernas
        for lado in [-1, 1]:
            glPushMatrix()
            glTranslatef(lado * 0.4, -1.0, 0)

            # Coxa
            glColor3f(0.15, 0.15, 0.15)
            glRotatef(lado * 10, 0, 0, 1)
            gluCylinder(quad, 0.25, 0.2, 0.8, 12, 1)

            # Joelho
            glTranslatef(0, 0, 0.8)
            gluSphere(quad, 0.25, 12, 12)

            # Canela
            glRotatef(10, 1, 0, 0)
            gluCylinder(quad, 0.2, 0.15, 0.7, 12, 1)

            # Pé
            glTranslatef(0, 0, 0.7)
            glScalef(1.0, 1.0, 1.5)
            gluSphere(quad, 0.2, 12, 12)

            glPopMatrix()

        # Detalhes do corpo (manchas em preto mais escuro)
        glColor3f(0.05, 0.05, 0.05)  # Preto mais escuro para as manchas
        for pos in [(0.5, 0.5, 0.3), (-0.5, 0.3, 0.4), (0.3, -0.4, 0.5), (-0.4, -0.2, 0.3)]:
            glPushMatrix()
            glTranslatef(*pos)
            glScalef(0.2, 0.2, 0.1)
            gluSphere(quad, 1.0, 8, 8)
            glPopMatrix()

        glPopMatrix()
        glDisable(GL_LIGHTING)
