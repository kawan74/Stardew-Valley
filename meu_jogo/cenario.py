from OpenGL.GL import *
from OpenGL.GLU import *
from objetos.chao import desenhar_chao
from objetos.casa import desenhar_casa
from objetos.nuvem import desenhar_nuvem

class Cenario:
    def __init__(self):
        glEnable(GL_DEPTH_TEST)

    def desenhar(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        desenhar_chao()
        desenhar_casa()
        desenhar_nuvem(-1, 2, -2)
        desenhar_nuvem(1.5, 2.5, -3)
