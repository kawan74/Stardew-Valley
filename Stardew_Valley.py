from OpenGL.GL import *
from OpenGL.GLU import *
import glfw
import time
import math
import random

class JogoOpenGL:
    def __init__(self, largura=800, altura=800, titulo='Jogo'):
        self.largura = largura
        self.altura = altura
        self.titulo = titulo
        self.window = None
        self.player_pos = [0, -0.7, 0]  # Posição do jogador
        self.camera_pos = [0, 0, 3]  # Câmera começa atrás do jogador
        self.yaw = -90.0 
        self.pitch = 0.0  
        self.sensibilidade = 0.1
        self.last_x = largura // 2
        self.last_y = altura // 2
        self.first_mouse = True
        self.modo_camera = '3D'
        self.habilitar_movimento_mouse = True
        self.camera_distance = 3.0  # Distância da câmera ao jogador
        self.camera_height = 1.5    # Altura da câmera em relação ao jogador
        self.galinhas = []  # Lista para armazenar as galinhas
        self.plantas = []   # Lista para armazenar as plantas
        self.inicializar_galinhas(5)  # Inicializar 5 galinhas
        self.inicializar_plantas(10)  # Inicializar 10 plantas

    def lerp_color(self, cor1, cor2, t):
        """
        Interpola linearmente entre duas cores.
        :param cor1: Primeira cor (R, G, B).
        :param cor2: Segunda cor (R, G, B).
        :param t: Fator de interpolação (0 a 1).
        :return: Cor interpolada (R, G, B).
        """
        return (
            cor1[0] + t * (cor2[0] - cor1[0]),
            cor1[1] + t * (cor2[1] - cor1[1]),
            cor1[2] + t * (cor2[2] - cor1[2])
        )

    def inicializar_galinhas(self, quantidade):
        for _ in range(quantidade):
            # Posição inicial aleatória dentro do espaço do chão
            x = random.uniform(-4.5, 4.5)
            z = random.uniform(-4.5, 4.5)
            self.galinhas.append({"posicao": [x, -1, z], "direcao": random.uniform(0, 360)})

    def inicializar_plantas(self, quantidade):
        for _ in range(quantidade):
            # Posição inicial aleatória dentro do espaço do chão
            x = random.uniform(-4.5, 4.5)
            z = random.uniform(-4.5, 4.5)
            self.plantas.append({"posicao": [x, -1, z]})

    def mover_galinhas(self):
        for galinha in self.galinhas:
            # Movimentar a galinha na direção atual
            velocidade = 0.01
            galinha["posicao"][0] += velocidade * math.cos(math.radians(galinha["direcao"]))
            galinha["posicao"][2] += velocidade * math.sin(math.radians(galinha["direcao"]))

            # Verificar limites do mapa
            if galinha["posicao"][0] < -4.5 or galinha["posicao"][0] > 4.5:
                galinha["direcao"] = 180 - galinha["direcao"]  # Inverter direção no eixo X
            if galinha["posicao"][2] < -4.5 or galinha["posicao"][2] > 4.5:
                galinha["direcao"] = -galinha["direcao"]  # Inverter direção no eixo Z

            # Mudar direção aleatoriamente de vez em quando
            if random.random() < 0.01:  # 1% de chance de mudar de direção
                galinha["direcao"] = random.uniform(0, 360)

    def iniciar_janela(self):
        if not glfw.init():
            return False

        # Obter o monitor principal para o modo de tela cheia
        monitor = glfw.get_primary_monitor()
        video_mode = glfw.get_video_mode(monitor)

        # Criar a janela em modo de tela cheia
        self.window = glfw.create_window(video_mode.size.width, video_mode.size.height, self.titulo, monitor, None)
        if not self.window:
            glfw.terminate()
            return False

        glfw.make_context_current(self.window)
        glfw.set_cursor_pos_callback(self.window, self.mouse_callback)
        glfw.set_key_callback(self.window, self.teclado_callback)
        return True
    
    def configurar_camera(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        if self.modo_camera == '3D':
            gluPerspective(100, self.largura / self.altura, 0.1, 100)
        else:
            glOrtho(-7, 7, -7, 7, -15, 10)
        glMatrixMode(GL_MODELVIEW)
    
    def configurar_cenario(self):
        glClearColor(0.1, 0.1, 0.3, 1.0)
        glEnable(GL_DEPTH_TEST)
    
    def iniciar_opengl(self):
        self.configurar_cenario()
        self.configurar_camera()

    def desenhar_chao(self):
        glColor3f(0.1, 0.7, 0.1)
        glBegin(GL_QUADS)
        glVertex3f(-5, -1, -5)
        glVertex3f(5, -1, -5)
        glVertex3f(5, -1, 5)
        glVertex3f(-5, -1, 5)
        glEnd()

    def desenhar_casa(self):
        # Ajustar a altura da casa para o nível do chão
        glPushMatrix()
        glTranslatef(0, -1, 0)  # Mover a casa para baixo para alinhar com o chão
        glRotatef(180, 0, 1, 0)  # Rotacionar a casa 180 graus no eixo Y

        # Corpo da casa
        glColor3f(0.9, 0.6, 0.3)
        body_vertices = [
            [-0.3, 0.0, -0.3], [0.3, 0.0, -0.3], [0.3, 0.4, -0.3], [-0.3, 0.4, -0.3],
            [-0.3, 0.0, 0.3], [0.3, 0.0, 0.3], [0.3, 0.4, 0.3], [-0.3, 0.4, 0.3]
        ]
        faces = [
            [0, 1, 2, 3], [4, 5, 6, 7], [0, 1, 5, 4],
            [2, 3, 7, 6], [1, 2, 6, 5], [0, 3, 7, 4]
        ]
        glBegin(GL_QUADS)
        for f in faces:
            for vertex in f:
                glVertex3fv(body_vertices[vertex])
        glEnd()
        
        # Telhado
        glColor3f(0.7, 0.1, 0.1)
        roof_vertices = [
            [-0.35, 0.4, -0.35], [0.35, 0.4, -0.35], [0.0, 0.6, 0.0],
            [-0.35, 0.4, 0.35], [0.35, 0.4, 0.35]
        ]
        roof_faces = [
            [0, 1, 2], [1, 4, 2], [4, 3, 2], [3, 0, 2]
        ]
        glBegin(GL_TRIANGLES)
        for f in roof_faces:
            for vertex in f:
                glVertex3fv(roof_vertices[vertex])
        glEnd()

        # Porta
        glColor3f(0.5, 0.3, 0.1)
        door_vertices = [
            [-0.05, 0.0, -0.301], [0.05, 0.0, -0.301], [0.05, 0.15, -0.301], [-0.05, 0.15, -0.301]
        ]
        glBegin(GL_QUADS)
        for vertex in door_vertices:
            glVertex3fv(vertex)
        glEnd()

        # Janelas
        glColor3f(0.7, 0.9, 1.0)
        windows = [
            [[-0.25, 0.1, -0.301], [-0.15, 0.1, -0.301], [-0.15, 0.2, -0.301], [-0.25, 0.2, -0.301]],
            [[0.15, 0.1, -0.301], [0.25, 0.1, -0.301], [0.25, 0.2, -0.301], [0.15, 0.2, -0.301]]
        ]
        for win in windows:
            glBegin(GL_QUADS)
            for vertex in win:
                glVertex3fv(vertex)
            glEnd()

        glPopMatrix()  # Restaurar a matriz de transformação anterior

    def desenhar_nuvem(self, x, y, z=0):
        glColor3f(1, 1, 1)
        for deslocamento in [0, 0.2, -0.2]:
            glBegin(GL_TRIANGLE_FAN)
            for i in range(360):
                angulo = math.radians(i)
                glVertex3f(x + 0.2 * math.cos(angulo) + deslocamento, y + 0.2 * math.sin(angulo), z)
            glEnd()

    def desenhar_cerca(self, x, z):
        glPushMatrix()
        glTranslatef(x, -1, z)  # Posicionar a cerca no chão
        glColor3f(0.5, 0.3, 0.1)  # Cor marrom para os postes
        post_positions = [-0.1, 0.1]
        for x_offset in post_positions:
            vertices = [
                [x_offset - 0.01, -0.2, -0.01], [x_offset + 0.01, -0.2, -0.01], [x_offset + 0.01, 0.1, -0.01], [x_offset - 0.01, 0.1, -0.01],
                [x_offset - 0.01, -0.2, 0.01], [x_offset + 0.01, -0.2, 0.01], [x_offset + 0.01, 0.1, 0.01], [x_offset - 0.01, 0.1, 0.01]
            ]
            faces = [
                [0, 1, 2, 3], [4, 5, 6, 7], [0, 1, 5, 4],
                [2, 3, 7, 6], [0, 3, 7, 4], [1, 2, 6, 5]
            ]
            glBegin(GL_QUADS)
            for face in faces:
                for vertex in face:
                    glVertex3fv(vertices[vertex])
            glEnd()

        glColor3f(0.6, 0.4, 0.2)  # Cor mais clara para as barras
        for y_offset in [-0.05, 0.05]:
            vertices = [
                [-0.1, y_offset - 0.01, -0.01], [0.1, y_offset - 0.01, -0.01], [0.1, y_offset + 0.01, -0.01], [-0.1, y_offset + 0.01, -0.01],
                [-0.1, y_offset - 0.01, 0.01], [0.1, y_offset - 0.01, 0.01], [0.1, y_offset + 0.01, 0.01], [-0.1, y_offset + 0.01, 0.01]
            ]
            faces = [
                [0, 1, 2, 3], [4, 5, 6, 7], [0, 1, 5, 4],
                [2, 3, 7, 6], [0, 3, 7, 4], [1, 2, 6, 5]
            ]
            glBegin(GL_QUADS)
            for face in faces:
                for vertex in face:
                    glVertex3fv(vertices[vertex])
            glEnd()
        glPopMatrix()

    def desenhar_planta(self, x, z):
        glPushMatrix()
        glTranslatef(x, -1, z)  # Posicionar a planta no chão
        # Tronco da planta (cilindro verde)
        glColor3f(0.0, 0.5, 0.0)
        glBegin(GL_QUADS)
        for vertex in [[-0.02, 0.0, -0.02], [0.02, 0.0, -0.02], [0.02, 0.3, -0.02], [-0.02, 0.3, -0.02],
                       [-0.02, 0.0, 0.02], [0.02, 0.0, 0.02], [0.02, 0.3, 0.02], [-0.02, 0.3, 0.02]]:
            glVertex3fv(vertex)
        glEnd()
        
        # Flor (esfera azul no topo)
        glColor3f(0.0, 0.0, 1.0)
        glPushMatrix()
        glTranslatef(0, 0.35, 0)
        quad = gluNewQuadric()
        gluSphere(quad, 0.1, 16, 16)
        glPopMatrix()
        glPopMatrix()

    def desenhar_galinha(self, x, z):
        glPushMatrix()
        glTranslatef(x, -1, z)  # Posicionar a galinha no chão
        # Corpo da galinha (paralelepípedo branco)
        glColor3f(1.0, 1.0, 1.0)
        body_vertices = [
            [-0.1, 0.0, -0.1], [0.1, 0.0, -0.1], [0.1, 0.2, -0.1], [-0.1, 0.2, -0.1],
            [-0.1, 0.0, 0.1], [0.1, 0.0, 0.1], [0.1, 0.2, 0.1], [-0.1, 0.2, 0.1]
        ]
        faces = [
            [0, 1, 2, 3], [4, 5, 6, 7], [0, 1, 5, 4],
            [2, 3, 7, 6], [1, 2, 6, 5], [0, 3, 7, 4]
        ]
        glBegin(GL_QUADS)
        for f in faces:
            for vertex in f:
                glVertex3fv(body_vertices[vertex])
        glEnd()
        
        # Crista da galinha (paralelepípedo vermelho - largura igual à cabeça)
        glColor3f(1.0, 0.0, 0.0)
        crest_vertices = [
            [-0.1, 0.2, -0.05], [0.1, 0.2, -0.05], [0.1, 0.25, -0.05], [-0.1, 0.25, -0.05],
            [-0.1, 0.2, 0.05], [0.1, 0.2, 0.05], [0.1, 0.25, 0.05], [-0.1, 0.25, 0.05]
        ]
        glBegin(GL_QUADS)
        for f in faces:
            for vertex in f:
                glVertex3fv(crest_vertices[vertex])
        glEnd()
        
        # Bico da galinha (paralelepípedo amarelo mais à frente)
        glColor3f(1.0, 1.0, 0.0)
        beak_vertices = [
            [0.05, 0.1, -0.15], [0.1, 0.1, -0.15], [0.1, 0.15, -0.15], [0.05, 0.15, -0.15]
        ]
        glBegin(GL_QUADS)
        for vertex in beak_vertices:
            glVertex3fv(vertex)
        glEnd()
        
        # Olhos da galinha (pequenos paralelepípedos pretos)
        glColor3f(0.0, 0.0, 0.0)
        eye_vertices = [
            [[-0.05, 0.15, -0.11], [-0.025, 0.15, -0.11], [-0.025, 0.175, -0.11], [-0.05, 0.175, -0.11]],
            [[0.025, 0.15, -0.11], [0.05, 0.15, -0.11], [0.05, 0.175, -0.11], [0.025, 0.175, -0.11]]
        ]
        for eye in eye_vertices:
            glBegin(GL_QUADS)
            for vertex in eye:
                glVertex3fv(vertex)
            glEnd()
        
        # Pernas da galinha (paralelepípedos pretos)
        glColor3f(0.0, 0.0, 0.0)
        leg_vertices = [
            [[-0.05, -0.1, -0.05], [-0.025, -0.1, -0.05], [-0.025, 0.0, -0.05], [-0.05, 0.0, -0.05],
             [-0.05, -0.1, 0.05], [-0.025, -0.1, 0.05], [-0.025, 0.0, 0.05], [-0.05, 0.0, 0.05]],
            [[0.025, -0.1, -0.05], [0.05, -0.1, -0.05], [0.05, 0.0, -0.05], [0.025, 0.0, -0.05],
             [0.025, -0.1, 0.05], [0.05, -0.1, 0.05], [0.05, 0.0, 0.05], [0.025, 0.0, 0.05]]
        ]
        for leg in leg_vertices:
            glBegin(GL_QUADS)
            for f in faces:
                for vertex in f:
                    glVertex3fv(leg[vertex])
            glEnd()
        glPopMatrix()

    def desenhar_cenario(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        tempo_decorrido = time.time() - self.tempo_inicio

        # Transição suave da cor do céu
        if tempo_decorrido < 15:
            cor_dia = (0.6, 0.8, 1.0)  
            cor_noite = (0.1, 0.1, 0.3)  
            t = tempo_decorrido / 30  # Tempo da transição
            cor_sky = self.lerp_color(cor_dia, cor_noite, t)
        else:
            cor_sky = (0.1, 0.1, 0.3)  

        glClearColor(cor_sky[0], cor_sky[1], cor_sky[2], 1.0)

        # Configurar a câmera para olhar para o jogador
        gluLookAt(
            self.camera_pos[0], self.camera_pos[1], self.camera_pos[2],  # Posição da câmera
            self.player_pos[0], self.player_pos[1] + 1, self.player_pos[2],  # Ponto para onde a câmera olha
            0, 1, 0  # Vetor UP
        )

        self.desenhar_chao()
        self.desenhar_casa()
        self.desenhar_nuvem(-1, 2, -2)
        self.desenhar_nuvem(1.5, 2.5, -3)
        
        # Desenhar o personagem na posição do jogador
        glPushMatrix()
        glTranslatef(self.player_pos[0], self.player_pos[1], self.player_pos[2])
        glRotatef(self.yaw + 90, 0, 1, 0)
        self.desenhar_personagem()
        glPopMatrix()

        # Desenhar cercas ao redor do cenário
        for x in range(-5, 6, 1):  # Cercas nas bordas x = -5 e x = 5
            self.desenhar_cerca(x, -5)
            self.desenhar_cerca(x, 5)
        for z in range(-5, 6, 1):  # Cercas nas bordas z = -5 e z = 5
            self.desenhar_cerca(-5, z)
            self.desenhar_cerca(5, z)

        # Desenhar as galinhas
        for galinha in self.galinhas:
            self.desenhar_galinha(galinha["posicao"][0], galinha["posicao"][2])

        # Desenhar as plantas
        for planta in self.plantas:
            self.desenhar_planta(planta["posicao"][0], planta["posicao"][2])

    def processar_entrada(self):
        move_speed = 0.05

        front_x = math.cos(math.radians(self.yaw))
        front_z = math.sin(math.radians(self.yaw))

        nova_pos_x = self.player_pos[0]
        nova_pos_z = self.player_pos[2]

        if glfw.get_key(self.window, glfw.KEY_W) == glfw.PRESS:
            nova_pos_x += move_speed * front_x
            nova_pos_z += move_speed * front_z
        if glfw.get_key(self.window, glfw.KEY_S) == glfw.PRESS:
            nova_pos_x -= move_speed * front_x
            nova_pos_z -= move_speed * front_z
        if glfw.get_key(self.window, glfw.KEY_D) == glfw.PRESS:
            nova_pos_x -= move_speed * front_z
            nova_pos_z += move_speed * front_x
        if glfw.get_key(self.window, glfw.KEY_A) == glfw.PRESS:
            nova_pos_x += move_speed * front_z
            nova_pos_z -= move_speed * front_x

        # Limitar andar dentro do espaço verde
        limite_min, limite_max = -4.5, 4.5  
        if limite_min <= nova_pos_x <= limite_max:
            self.player_pos[0] = nova_pos_x
        if limite_min <= nova_pos_z <= limite_max:
            self.player_pos[2] = nova_pos_z

        self.atualizar_camera()

    def mouse_callback(self, window, xpos, ypos):
        if not self.habilitar_movimento_mouse:
            return

        if self.first_mouse:
            self.last_x = xpos
            self.last_y = ypos
            self.first_mouse = False

        xoffset = (xpos - self.last_x) * self.sensibilidade
        yoffset = (self.last_y - ypos) * self.sensibilidade  

        self.last_x = xpos
        self.last_y = ypos

        self.yaw += xoffset
        self.pitch += yoffset

        self.pitch = max(-89.0, min(89.0, self.pitch))

    def teclado_callback(self, window, key, scancode, action, mods):
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(self.window, True)

        if key == glfw.KEY_M and action == glfw.PRESS:
            self.habilitar_movimento_mouse = not self.habilitar_movimento_mouse
            print("Movimento do mouse:", "Ativado" if self.habilitar_movimento_mouse else "Desativado")

    def atualizar_camera(self):
        # Calcular a posição da câmera baseada na posição do jogador
        camera_offset_x = -self.camera_distance * math.cos(math.radians(self.yaw)) * math.cos(math.radians(self.pitch))
        camera_offset_y = -self.camera_distance * math.sin(math.radians(self.pitch))
        camera_offset_z = -self.camera_distance * math.sin(math.radians(self.yaw)) * math.cos(math.radians(self.pitch))

        self.camera_pos[0] = self.player_pos[0] + camera_offset_x
        self.camera_pos[1] = self.player_pos[1] + camera_offset_y + self.camera_height
        self.camera_pos[2] = self.player_pos[2] + camera_offset_z

    def desenhar_personagem(self):
        # Corpo (tronco)
        glColor3f(0.2, 0.4, 0.8)  # Azul para a roupa
        glPushMatrix()
        glScalef(0.2, 0.3, 0.1)
        quad = gluNewQuadric()
        gluCylinder(quad, 1, 1, 1, 16, 16)
        glPopMatrix()

        # Cabeça
        glColor3f(0.8, 0.6, 0.4)  # Cor da pele
        glPushMatrix()
        glTranslatef(0, 0.4, 0)
        quad = gluNewQuadric()
        gluSphere(quad, 0.1, 16, 16)
        glPopMatrix()

        # Braços
        glColor3f(0.2, 0.4, 0.8)  # Azul para a roupa
        for x in [-0.15, 0.15]:  # Posição dos braços
            glPushMatrix()
            glTranslatef(x, 0.2, 0)
            glRotatef(90, 1, 0, 0)
            quad = gluNewQuadric()
            gluCylinder(quad, 0.03, 0.03, 0.2, 8, 8)
            glPopMatrix()

        # Pernas
        for x in [-0.07, 0.07]:  # Posição das pernas
            glPushMatrix()
            glTranslatef(x, -0.1, 0)
            glRotatef(90, 1, 0, 0)
            quad = gluNewQuadric()
            gluCylinder(quad, 0.04, 0.04, 0.2, 8, 8)
            glPopMatrix()

    def executar(self):
        if not self.iniciar_janela():
            return

        self.iniciar_opengl()
        self.tempo_inicio = time.time()  # Marca o início do jogo

        while not glfw.window_should_close(self.window):
            glfw.poll_events()
            self.processar_entrada()
            self.mover_galinhas()  # Atualizar a posição das galinhas
            self.desenhar_cenario()
            glfw.swap_buffers(self.window)

        glfw.terminate()

if __name__ == '__main__':
    jogo = JogoOpenGL()
    jogo.executar()