from OpenGL.GL import *
from OpenGL.GLU import *

class World:
    def __init__(self):
        self.sky_color = (0.6, 0.8, 1.0)
        self.house_pos = [0.0, -1.0, 2.0]  # Abaixando mais a casa para Y = -1.0

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

    def init_gl(self):
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(100, 800/800, 0.1, 100)
        glMatrixMode(GL_MODELVIEW)

    def draw(self):
        self.draw_ground()
        self.draw_house()
        self.draw_clouds()
        self.draw_fences()

    def draw_ground(self):
        glColor3f(0.1, 0.7, 0.1)
        glBegin(GL_QUADS)
        glVertex3f(-5, -1, -5)
        glVertex3f(5, -1, -5)
        glVertex3f(5, -1, 5)
        glVertex3f(-5, -1, 5)
        glEnd()

    def draw_house(self):
        glPushMatrix()
        # Translação para mover a casa para o final do cenário e rente ao chão
        glTranslatef(self.house_pos[0], self.house_pos[1], self.house_pos[2])
        # Rotação de 180 graus no eixo Y
        glRotatef(180, 0, 1, 0)
        # Escala para aumentar o tamanho da casa
        glScalef(3.0, 3.0, 3.0)
        
        # Parede frontal
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
        # Desenhar cercas horizontais (frontal e traseira)
        for x in range(-5, 6):  # Ajuste o range para aumentar a quantidade de cercas
            self.draw_fence_post(x, -1, -5, vertical=False)  # Cerca frontal
            self.draw_fence_post(x, -1, 5, vertical=False)   # Cerca traseira

        # Desenhar cercas laterais (esquerda e direita)
        for z in range(-5, 6):  # Ajuste o range para aumentar a quantidade de cercas
            glPushMatrix()
            glTranslatef(-5, -1, z)
            glRotatef(90, 0, 1, 0)  # Rotaciona 90 graus no eixo Y
            self.draw_fence_post(0, 0, 0, vertical=False)  # Cerca lateral esquerda
            glPopMatrix()

            glPushMatrix()
            glTranslatef(5, -1, z)
            glRotatef(90, 0, 1, 0)  # Rotaciona 90 graus no eixo Y
            self.draw_fence_post(0, 0, 0, vertical=False)  # Cerca lateral direita
            glPopMatrix()

    def draw_fence_post(self, x, y, z, vertical=False):
        glPushMatrix()
        glTranslatef(x, y, z)  # Ajuste para deixar rente ao chão
        
        glColor3f(0.5, 0.3, 0.1)  # Cor marrom para os postes
        post_positions = [-0.1, 0.1]
        for x in post_positions:
            vertices = [
                [x - 0.01, 0.0, -0.01], [x + 0.01, 0.0, -0.01], [x + 0.01, 0.3, -0.01], [x - 0.01, 0.3, -0.01],
                [x - 0.01, 0.0, 0.01], [x + 0.01, 0.0, 0.01], [x + 0.01, 0.3, 0.01], [x - 0.01, 0.3, 0.01]
            ]
            faces = [
                [0, 1, 2, 3], [4, 5, 6, 7], [0, 1, 5, 4], [2, 3, 7, 6], [0, 3, 7, 4], [1, 2, 6, 5]
            ]
            glBegin(GL_QUADS)
            for face in faces:
                for vertex in face:
                    glVertex3fv(vertices[vertex])
            glEnd()

        glColor3f(0.6, 0.4, 0.2)  # Cor mais clara para as barras
        for y_offset in [0.1, 0.2]:
            vertices = [
                [-0.1, y_offset - 0.01, -0.01], [0.1, y_offset - 0.01, -0.01], [0.1, y_offset + 0.01, -0.01], [-0.1, y_offset + 0.01, -0.01],
                [-0.1, y_offset - 0.01, 0.01], [0.1, y_offset - 0.01, 0.01], [0.1, y_offset + 0.01, 0.01], [-0.1, y_offset + 0.01, 0.01]
            ]
            faces = [
                [0, 1, 2, 3], [4, 5, 6, 7], [0, 1, 5, 4], [2, 3, 7, 6], [0, 3, 7, 4], [1, 2, 6, 5]
            ]
            glBegin(GL_QUADS)
            for face in faces:
                for vertex in face:
                    glVertex3fv(vertices[vertex])
            glEnd()
        
        glPopMatrix()