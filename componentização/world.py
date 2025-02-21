from OpenGL.GL import *
from OpenGL.GLU import *
import glfw
import time
import os
from PIL import Image

class World:
    def __init__(self):
        self.sky_color = (0.6, 0.8, 1.0)  # Cor inicial do céu (azul claro)
        self.house_pos = [0.0, -1.0, 2.0]  # Posição da casa
        self.ground_texture = None  # Variável para armazenar a textura do chão

    def lerp_color(self, cor1, cor2, t):
        """
        Interpola linearmente entre duas cores.
        """
        return (
            cor1[0] + t * (cor2[0] - cor1[0]),
            cor1[1] + t * (cor2[1] - cor1[1]),
            cor1[2] + t * (cor2[2] - cor1[2])
        )

    def update_sky_color(self, tempo_decorrido):
        """
        Atualiza a cor do céu com base no tempo decorrido.
        """
        if tempo_decorrido < 15:
            cor_dia = (0.6, 0.8, 1.0)  # Azul claro (dia)
            cor_noite = (0.1, 0.1, 0.3)  # Azul escuro (noite)
            t = tempo_decorrido / 30  # Interpolação baseada no tempo
            self.sky_color = self.lerp_color(cor_dia, cor_noite, t)
        else:
            self.sky_color = (0.1, 0.1, 0.3)  # Cor fixa para noite
        
        # Define a cor de fundo (céu) com base na cor atual
        glClearColor(self.sky_color[0], self.sky_color[1], self.sky_color[2], 1.0)

    def carregar_textura(self, caminho_imagem: str) -> int:
        """Carrega uma textura a partir de um arquivo de imagem."""
        if not os.path.exists(caminho_imagem):
            print(f"Erro: Arquivo de textura não encontrado em {caminho_imagem}")
            return 0

        try:
            imagem = Image.open(caminho_imagem)
        except Exception as erro:
            print(f"Erro ao carregar a imagem '{caminho_imagem}': {erro}")
            return 0

        imagem = imagem.transpose(Image.FLIP_TOP_BOTTOM)
        imagem = imagem.convert("RGBA")
        largura, altura = imagem.size
        dados_imagem = imagem.tobytes()

        id_textura = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, id_textura)

        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, largura, altura, 0, GL_RGBA, GL_UNSIGNED_BYTE, dados_imagem)
        
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

        glBindTexture(GL_TEXTURE_2D, 0)
        print(f"Textura carregada com sucesso: {caminho_imagem}")
        return id_textura

    def init_gl(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_TEXTURE_2D)  # Habilitar texturas
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(100, 800/800, 0.1, 100)
        glMatrixMode(GL_MODELVIEW)
        
        # Carregar a textura do chão
        self.ground_texture = self.carregar_textura('texturas/chao.png')
        if self.ground_texture == 0:
            print("Erro ao carregar a textura do chão.")

    def draw_ground(self):
        if self.ground_texture:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.ground_texture)
            print("Textura do chão vinculada.")

        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0); glVertex3f(-5, -1, -5)
        glTexCoord2f(10.0, 0.0); glVertex3f(5, -1, -5)
        glTexCoord2f(10.0, 10.0); glVertex3f(5, -1, 5)
        glTexCoord2f(0.0, 10.0); glVertex3f(-5, -1, 5)
        glEnd()

        if self.ground_texture:
            glDisable(GL_TEXTURE_2D)

    def draw_house(self):
        glPushMatrix()
        glTranslatef(self.house_pos[0], self.house_pos[1], self.house_pos[2])
        glRotatef(180, 0, 1, 0)
        glScalef(3.0, 3.0, 3.0)

        # Desenhar a casa sem textura
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
        
        glPopMatrix()

    def draw_clouds(self):
        def draw_single_cloud(x, y, z):
            glColor3f(1.0, 1.0, 1.0)  # Branco
            glPushMatrix()
            glTranslatef(x, y, z)
            
            # Várias esferas para formar uma nuvem
            positions = [(0,0,0), (0.3,0.1,0), (-0.3,0.1,0), (0.15,-0.1,0), (-0.15,-0.1,0)]
            for pos in positions:
                glPushMatrix()
                glTranslatef(pos[0], pos[1], pos[2])
                quad = gluNewQuadric()
                gluSphere(quad, 0.2, 16, 16)
                glPopMatrix()
            
            glPopMatrix()

        # Desenhar múltiplas nuvens em posições diferentes
        draw_single_cloud(-1, 2, -2)
        draw_single_cloud(1.5, 2.5, -3)
        draw_single_cloud(-2, 2.2, -4)

    def draw_fences(self):
        glColor3f(0.6, 0.3, 0.0)  # Marrom para a cerca
        
        # Desenha cercas ao redor da área do jogo
        for x in range(-5, 6, 1):
            # Cerca frontal
            self.draw_fence_post(x, -1, -5)
            # Cerca traseira
            self.draw_fence_post(x, -1, 5)
            
        for z in range(-5, 6, 1):
            # Cerca lateral esquerda
            self.draw_fence_post(-5, -1, z)
            # Cerca lateral direita
            self.draw_fence_post(5, -1, z)

    def draw_fence_post(self, x, y, z):
        glPushMatrix()
        glTranslatef(x, y, z)
        
        # Poste vertical
        glPushMatrix()
        glScalef(0.1, 1.0, 0.1)
        quad = gluNewQuadric()
        gluCylinder(quad, 0.5, 0.5, 1, 8, 1)
        glPopMatrix()
        
        # Travessa horizontal
        glPushMatrix()
        glTranslatef(0, 0.3, 0)
        glRotatef(90, 0, 1, 0)
        glScalef(0.1, 0.1, 1.0)
        quad = gluNewQuadric()
        gluCylinder(quad, 0.5, 0.5, 1, 8, 1)
        glPopMatrix()
        
        glPopMatrix()

    def draw(self):
        self.draw_ground()
        self.draw_house()
        self.draw_clouds()
        self.draw_fences()

class JogoOpenGL:
    def __init__(self, largura=800, altura=800, titulo='Jogo'):
        self.largura = largura
        self.altura = altura
        self.titulo = titulo
        self.window = None
        self.world = World()  # Instância da classe World
        self.tempo_inicio = time.time()  # Tempo inicial do jogo

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
        pass  # Implemente a lógica do mouse, se necessário

    def teclado_callback(self, window, key, scancode, action, mods):
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(self.window, True)

    def processar_entrada(self):
        pass  # Implemente a lógica de entrada, se necessário

    def desenhar_cenario(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Atualiza a cor do céu com base no tempo decorrido
        tempo_decorrido = time.time() - self.tempo_inicio
        self.world.update_sky_color(tempo_decorrido)

        # Configurar a câmera
        gluLookAt(0, 0, 10, 0, 0, 0, 0, 1, 0)

        # Desenhar o cenário
        self.world.draw()

    def executar(self):
        if not self.iniciar_janela():
            return

        self.world.init_gl()  # Inicializa o OpenGL

        while not glfw.window_should_close(self.window):
            glfw.poll_events()
            self.processar_entrada()
            self.desenhar_cenario()
            glfw.swap_buffers(self.window)

        glfw.terminate()

if __name__ == "__main__":
    jogo = JogoOpenGL()
    jogo.executar()