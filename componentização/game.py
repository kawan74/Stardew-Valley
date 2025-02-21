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
        self.player.draw()
        self.entities.draw()

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
