import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from camera import Camera
from cenario import Cenario

class JogoOpenGL:
    def __init__(self, largura=800, altura=800, titulo='Jogo'):
        self.largura = largura
        self.altura = altura
        self.titulo = titulo
        self.window = None
        self.camera = Camera()
        self.cenario = None  # Instanciado depois que o contexto for criado

    def iniciar_janela(self):
        if not glfw.init():
            return False

        self.window = glfw.create_window(self.largura, self.altura, self.titulo, None, None)
        if not self.window:
            glfw.terminate()
            return False

        glfw.make_context_current(self.window)
        self.cenario = Cenario()  # Agora criamos o cenario após o contexto estar ativo
        return True

    def executar(self):
        if not self.iniciar_janela():
            return

        while not glfw.window_should_close(self.window):
            glfw.poll_events()
            self.cenario.desenhar()
            glfw.swap_buffers(self.window)

        glfw.terminate()
