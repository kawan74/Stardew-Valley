from OpenGL.GL import *
from OpenGL.GLU import *
from objetos.chao import desenhar_chao
from objetos.casa import desenhar_casa
from objetos.nuvem import desenhar_nuvem

class Cenario:
    def __init__(self):
        glEnable(GL_DEPTH_TEST)  # Ativa o teste de profundidade para 3D
        self.setup_perspectiva()

    def setup_perspectiva(self):
        """Configura a projeção 3D da câmera"""
        glMatrixMode(GL_PROJECTION)  # Altera para a matriz de projeção
        glLoadIdentity()  # Limpa a matriz de projeção
        gluPerspective(45, 800 / 600, 0.1, 100.0)  # Define a perspectiva 3D
        glMatrixMode(GL_MODELVIEW)  # Retorna para a matriz de visualização

    def desenhar_ceu(self):
        """Desenha a skybox (céu e chão) em 3D"""
        # Desenha o céu
        glPushMatrix()
        glTranslatef(0.0, 0.0, -50.0)  # Posiciona a skybox a uma distância
        self.desenhar_cubo_ceu()
        glPopMatrix()

        # Desenha o chão (em 3D)
        self.desenhar_chao()

    def desenhar_chao(self):
        """Desenha o chão em 3D com cor verde"""
        glPushMatrix()
        glTranslatef(0.0, -1.0, 0.0)  # Ajusta a posição do chão
        glBegin(GL_QUADS)
        glColor3f(0.0, 1.0, 0.0)  # Verde
        glVertex3f(-50.0, 0.0, -50.0)
        glVertex3f(50.0, 0.0, -50.0)
        glVertex3f(50.0, 0.0, 50.0)
        glVertex3f(-50.0, 0.0, 50.0)
        glEnd()
        glPopMatrix()

    def desenhar_cubo_ceu(self):
        """Desenha um cubo que representa o céu em 3D, cor azul"""
        glBegin(GL_QUADS)

        # Face frontal (azul)
        glColor3f(0.0, 0.0, 1.0)  # Azul
        glVertex3f(-50.0, 50.0, -50.0)
        glVertex3f(50.0, 50.0, -50.0)
        glVertex3f(50.0, -50.0, -50.0)
        glVertex3f(-50.0, -50.0, -50.0)

        # Face traseira (azul)
        glColor3f(0.0, 0.0, 1.0)
        glVertex3f(-50.0, -50.0, 50.0)
        glVertex3f(50.0, -50.0, 50.0)
        glVertex3f(50.0, 50.0, 50.0)
        glVertex3f(-50.0, 50.0, 50.0)

        # Face direita (azul)
        glColor3f(0.0, 0.0, 1.0)
        glVertex3f(50.0, 50.0, -50.0)
        glVertex3f(50.0, 50.0, 50.0)
        glVertex3f(50.0, -50.0, 50.0)
        glVertex3f(50.0, -50.0, -50.0)

        # Face esquerda (azul)
        glColor3f(0.0, 0.0, 1.0)
        glVertex3f(-50.0, -50.0, -50.0)
        glVertex3f(-50.0, -50.0, 50.0)
        glVertex3f(-50.0, 50.0, 50.0)
        glVertex3f(-50.0, 50.0, -50.0)

        # Face superior (azul claro)
        glColor3f(0.5, 0.5, 1.0)  # Azul claro
        glVertex3f(-50.0, 50.0, -50.0)
        glVertex3f(50.0, 50.0, -50.0)
        glVertex3f(50.0, 50.0, 50.0)
        glVertex3f(-50.0, 50.0, 50.0)

        # Face inferior (azul escuro)
        glColor3f(0.2, 0.2, 0.5)  # Azul escuro
        glVertex3f(-50.0, -50.0, -50.0)
        glVertex3f(50.0, -50.0, -50.0)
        glVertex3f(50.0, -50.0, 50.0)
        glVertex3f(-50.0, -50.0, 50.0)

        glEnd()

    def desenhar(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Desenha a skybox (céu) e o chão em 3D
        self.desenhar_ceu()

        # Desenha os outros objetos no cenário
        desenhar_casa()
        desenhar_nuvem(-1, 2, -2)
        desenhar_nuvem(1.5, 2.5, -3)
