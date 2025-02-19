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
        self.camera_pos = [0, 0, -3]
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

        self.window = glfw.create_window(self.largura, self.altura, self.titulo, None, None)
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
        glColor3f(0.8, 0.5, 0.2)
        glBegin(GL_QUADS)
        glVertex3f(-0.3, -1, 0.0)
        glVertex3f(-0.3, -0.6, 0.0)
        glVertex3f(0.3, -0.6, 0.0)
        glVertex3f(0.3, -1, 0.0)
        glEnd()

        # Telhado
        glColor3f(0.5, 0.2, 0.1)
        glBegin(GL_TRIANGLES)
        glVertex3f(-0.35, -0.6, 0.0)
        glVertex3f(0.35, -0.6, 0.0)
        glVertex3f(0.0, -0.3, 0.0)
        glEnd()

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
        move_speed = 0.05

        front_x = math.cos(math.radians(self.yaw))
        front_z = math.sin(math.radians(self.yaw))

        if glfw.get_key(self.window, glfw.KEY_W) == glfw.PRESS:
            self.camera_pos[0] += move_speed * front_x
            self.camera_pos[2] += move_speed * front_z
        if glfw.get_key(self.window, glfw.KEY_S) == glfw.PRESS:
            self.camera_pos[0] -= move_speed * front_x
            self.camera_pos[2] -= move_speed * front_z
        if glfw.get_key(self.window, glfw.KEY_A) == glfw.PRESS:
            self.camera_pos[0] -= move_speed * front_z
            self.camera_pos[2] += move_speed * front_x
        if glfw.get_key(self.window, glfw.KEY_D) == glfw.PRESS:
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
