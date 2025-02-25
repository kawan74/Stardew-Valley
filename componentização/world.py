from OpenGL.GL import *
from OpenGL.GLU import *
import glfw
import time
import numpy as np
from OpenGL.GLU import * 

class World:
    def __init__(self):
        self.sky_color = (0.6, 0.8, 1.0)
        self.house_pos = [0.0, -1.0, 2.0]
        self.ground_texture = None

    def lerp_color(self, cor1, cor2, t):
        return (
            cor1[0] + t * (cor2[0] - cor1[0]),
            cor1[1] + t * (cor2[1] - cor1[1]),
            cor1[2] + t * (cor2[2] - cor1[2])
        )

    def update_sky_color(self, tempo_decorrido):
        if tempo_decorrido < 15:
            cor_dia = (0.6, 0.8, 1.0)
            cor_noite = (0.1, 0.1, 0.3)
            t = tempo_decorrido / 30
            self.sky_color = self.lerp_color(cor_dia, cor_noite, t)
        else:
            self.sky_color = (0.1, 0.1, 0.3)

        glClearColor(self.sky_color[0], self.sky_color[1], self.sky_color[2], 1.0)

    def generate_grass_texture(self, width=256, height=256):
        texture_data = np.zeros((height, width, 3), dtype=np.uint8)

        for y in range(height):
            for x in range(width):
                green_shade = np.random.randint(130, 180)
                texture_data[y, x] = [34, green_shade, 34]

                if np.random.random() < 0.05:
                    texture_data[y, x] = [255, 0, 0]

        return texture_data.tobytes()

    def carregar_textura_grama(self):
        texture_data = self.generate_grass_texture()

        tex = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

        glTexImage2D(
            GL_TEXTURE_2D,
            0,
            GL_RGB,
            256, 256,
            0,
            GL_RGB,
            GL_UNSIGNED_BYTE,
            texture_data
        )

        error = glGetError()
        if error != GL_NO_ERROR:
            print(f"Erro ao carregar a textura: {gluErrorString(error)}")

        glBindTexture(GL_TEXTURE_2D, 0)

        if tex == 0:
            print("Erro ao carregar a textura do chão.")
        else:
            print(f"Textura de grama carregada com sucesso: {tex}")

        return tex

    def init_gl(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_TEXTURE_2D)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(100, 800 / 800, 0.1, 100)
        glMatrixMode(GL_MODELVIEW)

        self.ground_texture = self.carregar_textura_grama()

        if self.ground_texture == 0:
            print("Erro ao carregar a textura do chão.")
        else:
            print("Textura de grama carregada com sucesso.")

    def draw_ground(self):
        if self.ground_texture:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.ground_texture)

            glColor3f(1.0, 1.0, 1.0)

            glBegin(GL_QUADS)
            glTexCoord2f(0.0, 0.0); glVertex3f(-5, -1, -5)
            glTexCoord2f(1.0, 0.0); glVertex3f(5, -1, -5)
            glTexCoord2f(1.0, 1.0); glVertex3f(5, -1, 5)
            glTexCoord2f(0.0, 1.0); glVertex3f(-5, -1, 5)
            glEnd()

            glBindTexture(GL_TEXTURE_2D, 0)
            glDisable(GL_TEXTURE_2D)
        else:
            print("Textura do chão não carregada, não é possível desenhar o chão.")

    def draw_house(self):
        glPushMatrix()
        glTranslatef(self.house_pos[0], self.house_pos[1], self.house_pos[2])
        glRotatef(180, 0, 1, 0)
        glScalef(3.0, 3.0, 3.0)

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

        glColor3f(0.5, 0.3, 0.1)
        door_vertices = [
            [-0.05, 0.0, -0.301], [0.05, 0.0, -0.301], [0.05, 0.15, -0.301], [-0.05, 0.15, -0.301]
        ]
        glBegin(GL_QUADS)
        for vertex in door_vertices:
            glVertex3fv(vertex)
        glEnd()

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
            glColor3f(1.0, 1.0, 1.0)  
            glPushMatrix()
            glTranslatef(x, y, z)
            
            positions = [(0,0,0), (0.3,0.1,0), (-0.3,0.1,0), (0.15,-0.1,0), (-0.15,-0.1,0)]
            for pos in positions:
                glPushMatrix()
                glTranslatef(pos[0], pos[1], pos[2])
                quad = gluNewQuadric()
                gluSphere(quad, 0.2, 16, 16)
                glPopMatrix()
            
            glPopMatrix()

        draw_single_cloud(-1, 2, -2)
        draw_single_cloud(1.5, 2.5, -3)
        draw_single_cloud(-2, 2.2, -4)

    def draw_fences(self):
        glColor3f(0.6, 0.3, 0.0)  
        
        for x in range(-5, 6, 1):
            self.draw_fence_post(x, -1, -5)
        
            self.draw_fence_post(x, -1, 5)
            
        for z in range(-5, 6, 1):
            self.draw_fence_post(-5, -1, z)
        
            self.draw_fence_post(5, -1, z)

    def draw_fence_post(self, x, y, z):
        glPushMatrix()
        glTranslatef(x, y, z)
        
        if x == -5 or x == 5:
            glRotatef(90, 0, 1, 0)

        glPushMatrix()
        glScalef(0.1, 1.0, 0.1)
        glBegin(GL_QUADS)
        glVertex3f(-0.5, 0.0, 0.5)
        glVertex3f(0.5, 0.0, 0.5)
        glVertex3f(0.5, 1.0, 0.5)
        glVertex3f(-0.5, 1.0, 0.5)
        glVertex3f(-0.5, 0.0, -0.5)
        glVertex3f(0.5, 0.0, -0.5)
        glVertex3f(0.5, 1.0, -0.5)
        glVertex3f(-0.5, 1.0, -0.5)
        glVertex3f(-0.5, 0.0, -0.5)
        glVertex3f(-0.5, 0.0, 0.5)
        glVertex3f(-0.5, 1.0, 0.5)
        glVertex3f(-0.5, 1.0, -0.5)
        glVertex3f(0.5, 0.0, -0.5)
        glVertex3f(0.5, 0.0, 0.5)
        glVertex3f(0.5, 1.0, 0.5)
        glVertex3f(0.5, 1.0, -0.5)
        glVertex3f(-0.5, 1.0, -0.5)
        glVertex3f(0.5, 1.0, -0.5)
        glVertex3f(0.5, 1.0, 0.5)
        glVertex3f(-0.5, 1.0, 0.5)
        glVertex3f(-0.5, 0.0, -0.5)
        glVertex3f(0.5, 0.0, -0.5)
        glVertex3f(0.5, 0.0, 0.5)
        glVertex3f(-0.5, 0.0, 0.5)
        glEnd()
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(0, 0.5, 0)
        glScalef(1.0, 0.1, 0.1)
        glBegin(GL_QUADS)
        glVertex3f(-0.5, -0.5, 0.5)
        glVertex3f(0.5, -0.5, 0.5)
        glVertex3f(0.5, 0.5, 0.5)
        glVertex3f(-0.5, 0.5, 0.5)
        glVertex3f(-0.5, -0.5, -0.5)
        glVertex3f(0.5, -0.5, -0.5)
        glVertex3f(0.5, 0.5, -0.5)
        glVertex3f(-0.5, 0.5, -0.5)
        glVertex3f(-0.5, -0.5, -0.5)
        glVertex3f(-0.5, -0.5, 0.5)
        glVertex3f(-0.5, 0.5, 0.5)
        glVertex3f(-0.5, 0.5, -0.5)
        glVertex3f(0.5, -0.5, -0.5)
        glVertex3f(0.5, -0.5, 0.5)
        glVertex3f(0.5, 0.5, 0.5)
        glVertex3f(0.5, 0.5, -0.5)
        glVertex3f(-0.5, 0.5, -0.5)
        glVertex3f(0.5, 0.5, -0.5)
        glVertex3f(0.5, 0.5, 0.5)
        glVertex3f(-0.5, 0.5, 0.5)
        glVertex3f(-0.5, -0.5, -0.5)
        glVertex3f(0.5, -0.5, -0.5)
        glVertex3f(0.5, -0.5, 0.5)
        glVertex3f(-0.5, -0.5, 0.5)
        glEnd()
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
        self.world = World()  
        self.tempo_inicio = time.time()  

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

    def teclado_callback(self, window, key, scancode, action, mods):
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(self.window, True)

    def desenhar_cenario(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        tempo_decorrido = time.time() - self.tempo_inicio
        self.world.update_sky_color(tempo_decorrido)

        gluLookAt(0, 0, 10, 0, 0, 0, 0, 1, 0)

        self.world.draw()

    def executar(self):
        if not self.iniciar_janela():
            return

        self.world.init_gl()  

        while not glfw.window_should_close(self.window):
            glfw.poll_events()
            self.processar_entrada()
            self.desenhar_cenario()
            glfw.swap_buffers(self.window)

        glfw.terminate()

if __name__ == "__main__":
    jogo = JogoOpenGL()
    jogo.executar()
    
    