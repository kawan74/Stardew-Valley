import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from camera import Camera
from cenario import Cenario
import time

class JogoOpenGL:
    def __init__(self, largura=800, altura=800, titulo='Jogo'):
        self.largura = largura
        self.altura = altura
        self.titulo = titulo
        self.window = None
        self.camera = Camera()
        self.cenario = None  # Instanciado depois que o contexto for criado
        self.last_x = 400
        self.last_y = 400
        self.first_mouse = True

    def iniciar_janela(self):
        if not glfw.init():
            return False

        self.window = glfw.create_window(self.largura, self.altura, self.titulo, None, None)
        if not self.window:
            glfw.terminate()
            return False

        glfw.make_context_current(self.window)
        self.cenario = Cenario()  # Agora criamos o cenario após o contexto estar ativo

        # Habilita o input de mouse
        glfw.set_cursor_pos_callback(self.window, self.mouse_callback)
        return True

    def mouse_callback(self, window, xpos, ypos):
        """Processa os movimentos do mouse"""
        if self.camera.first_mouse:
            self.last_x = xpos
            self.last_y = ypos
            self.camera.first_mouse = False

        x_offset = xpos - self.last_x
        y_offset = self.last_y - ypos  # Reverte o eixo Y para ficar correto
        self.last_x = xpos
        self.last_y = ypos

        self.camera.process_mouse_movement(x_offset, y_offset)

    def processar_entrada(self, delta_time):
        """Processa os inputs do teclado"""
        self.camera.update(delta_time)

    def executar(self):
        if not self.iniciar_janela():
            return

        last_time = time.time()
        while not glfw.window_should_close(self.window):
            # Calcula o delta_time
            current_time = time.time()
            delta_time = current_time - last_time
            last_time = current_time

            glfw.poll_events()
            self.processar_entrada(delta_time)  # Processa os inputs (teclado e mouse)
            self.cenario.desenhar()

            # Atualiza a matriz de visualização da câmera
            glLoadIdentity()
            gluLookAt(self.camera.pos[0], self.camera.pos[1], self.camera.pos[2], 
                      self.camera.pos[0] + self.camera.front[0], 
                      self.camera.pos[1] + self.camera.front[1], 
                      self.camera.pos[2] + self.camera.front[2], 
                      self.camera.up[0], self.camera.up[1], self.camera.up[2])

            glfw.swap_buffers(self.window)

        glfw.terminate()
