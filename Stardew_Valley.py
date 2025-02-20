from OpenGL.GL import *
from OpenGL.GLU import *
import glfw
import time
import math

class JogoOpenGL:
    def __init__(self, largura=800, altura=800, titulo='Jogo'):
        self.largura = largura
        self.altura = altura
        self.titulo = titulo
        self.window = None
        self.camera_pos = [0, -0.7, -3]
        self.yaw = -90.0 
        self.pitch = 0.0  
        self.sensibilidade = 0.1
        self.last_x = largura // 2
        self.last_y = altura // 2
        self.first_mouse = True
        self.modo_camera = '3D'
        self.habilitar_movimento_mouse = True  

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

    def desenhar_cenario(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Configuração da câmera
        look_x = math.cos(math.radians(self.yaw)) * math.cos(math.radians(self.pitch))
        look_y = math.sin(math.radians(self.pitch))
        look_z = math.sin(math.radians(self.yaw)) * math.cos(math.radians(self.pitch))

        gluLookAt(
            self.camera_pos[0], self.camera_pos[1], self.camera_pos[2],
            self.camera_pos[0] + look_x, self.camera_pos[1] + look_y, self.camera_pos[2] + look_z,
            0, 1, 0
        )

        self.desenhar_chao()
        self.desenhar_casa()
        self.desenhar_nuvem(-1, 2, -2)
        self.desenhar_nuvem(1.5, 2.5, -3)

    def processar_entrada(self):
        move_speed = 0.005

        front_x = math.cos(math.radians(self.yaw))
        front_z = math.sin(math.radians(self.yaw))

        if glfw.get_key(self.window, glfw.KEY_W) == glfw.PRESS:
            self.camera_pos[0] += move_speed * front_x
            self.camera_pos[2] += move_speed * front_z
        if glfw.get_key(self.window, glfw.KEY_S) == glfw.PRESS:
            self.camera_pos[0] -= move_speed * front_x
            self.camera_pos[2] -= move_speed * front_z
        if glfw.get_key(self.window, glfw.KEY_D) == glfw.PRESS:
            self.camera_pos[0] -= move_speed * front_z
            self.camera_pos[2] += move_speed * front_x
        if glfw.get_key(self.window, glfw.KEY_A) == glfw.PRESS:
            self.camera_pos[0] += move_speed * front_z
            self.camera_pos[2] -= move_speed * front_x

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

    def executar(self):
        if not self.iniciar_janela():
            return

        self.iniciar_opengl()
        while not glfw.window_should_close(self.window):
            glfw.poll_events()
            self.processar_entrada()
            self.desenhar_cenario()
            glfw.swap_buffers(self.window)

        glfw.terminate()

if __name__ == '__main__':
    jogo = JogoOpenGL()
    jogo.executar()
