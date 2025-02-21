from OpenGL.GL import *
from OpenGL.GLU import *

class World:
    def __init__(self):
        self.sky_color = (0.6, 0.8, 1.0)

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
        # Parede frontal
        glColor3f(0.8, 0.6, 0.4)  # Marrom claro
        glBegin(GL_QUADS)
        glVertex3f(-1.5, -1, -2)
        glVertex3f(1.5, -1, -2)
        glVertex3f(1.5, 1, -2)
        glVertex3f(-1.5, 1, -2)
        glEnd()

        # Telhado
        glColor3f(0.5, 0.2, 0.0)  # Marrom escuro
        glBegin(GL_TRIANGLES)
        glVertex3f(-1.7, 1, -1.8)
        glVertex3f(1.7, 1, -1.8)
        glVertex3f(0, 2, -2)
        glEnd()

        # Porta
        glColor3f(0.4, 0.2, 0.0)  # Marrom mais escuro
        glBegin(GL_QUADS)
        glVertex3f(-0.3, -1, -1.99)
        glVertex3f(0.3, -1, -1.99)
        glVertex3f(0.3, 0.3, -1.99)
        glVertex3f(-0.3, 0.3, -1.99)
        glEnd()

        # Janela
        glColor3f(0.8, 0.8, 1.0)  # Azul claro
        glBegin(GL_QUADS)
        glVertex3f(0.6, 0, -1.99)
        glVertex3f(1.1, 0, -1.99)
        glVertex3f(1.1, 0.5, -1.99)
        glVertex3f(0.6, 0.5, -1.99)
        glEnd()

        # Grade da janela
        glColor3f(0.4, 0.2, 0.0)
        glLineWidth(2.0)
        glBegin(GL_LINES)
        # Linha vertical
        glVertex3f(0.85, 0, -1.98)
        glVertex3f(0.85, 0.5, -1.98)
        # Linha horizontal
        glVertex3f(0.6, 0.25, -1.98)
        glVertex3f(1.1, 0.25, -1.98)
        glEnd()

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