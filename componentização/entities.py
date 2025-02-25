import random
import math
from OpenGL.GL import *
from OpenGL.GLU import *

class Entities:
    def __init__(self):
        self.galinhas = []
        self.plantas = []
        self.inicializar_galinhas(5)
        self.inicializar_plantas(10)

    def inicializar_galinhas(self, quantidade):
        for _ in range(quantidade):
            x = random.uniform(-4.5, 4.5)
            z = random.uniform(-4.5, 4.5)
            self.galinhas.append({"posicao": [x, -1, z], "direcao": random.uniform(0, 360)})

    def inicializar_plantas(self, quantidade):
        for _ in range(quantidade):
            x = random.uniform(-4.5, 4.5)
            z = random.uniform(-4.5, 4.5)
            self.plantas.append({"posicao": [x, -1, z]})

    def update(self):
        self.mover_galinhas()

    def mover_galinhas(self):
        for galinha in self.galinhas:
            velocidade = 0.01
            galinha["posicao"][0] += velocidade * math.cos(math.radians(galinha["direcao"]))
            galinha["posicao"][2] += velocidade * math.sin(math.radians(galinha["direcao"]))

            if galinha["posicao"][0] < -4.5 or galinha["posicao"][0] > 4.5:
                galinha["direcao"] = 180 - galinha["direcao"]
            if galinha["posicao"][2] < -4.5 or galinha["posicao"][2] > 4.5:
                galinha["direcao"] = -galinha["direcao"]

            if random.random() < 0.01:
                galinha["direcao"] = random.uniform(0, 360)

    def draw(self):
        for galinha in self.galinhas:
            self.draw_galinha(galinha["posicao"][0], galinha["posicao"][2])
        for planta in self.plantas:
            self.draw_planta(planta["posicao"][0], planta["posicao"][2])

    def draw_galinha(self, x, z):
        glPushMatrix()
        glTranslatef(x, -0.8, z)
        
        glColor3f(1.0, 1.0, 1.0)
        quad = gluNewQuadric()
        glPushMatrix()
        glScalef(1.0, 0.8, 1.0)
        gluSphere(quad, 0.15, 8, 8)
        glPopMatrix()
        
        glPushMatrix()
        glRotatef(90, 0, 1, 0)
        glTranslatef(0.1, 0.1, 0)
        gluSphere(quad, 0.08, 8, 8)
        glPopMatrix()
        
        glColor3f(1.0, 0.5, 0.0)
        glPushMatrix()
        glTranslatef(0.18, 0.1, 0)
        glScalef(0.5, 0.5, 0.5)
        gluSphere(quad, 0.05, 8, 8)
        glPopMatrix()
        
        glColor3f(1.0, 0.5, 0.0)
        for offset in [-0.05, 0.05]:
            glPushMatrix()
            glTranslatef(0, -0.1, offset)
            glRotatef(90, 1, 0, 0)
            gluCylinder(quad, 0.02, 0.02, 0.1, 4, 1)
            glPopMatrix()
        
        glPopMatrix()

    def draw_planta(self, x, z):
        glPushMatrix()
        glTranslatef(x, -1, z)
        
        glColor3f(0.0, 0.5, 0.0)
        quad = gluNewQuadric()
        glPushMatrix()
        glRotatef(-90, 1, 0, 0)
        gluCylinder(quad, 0.02, 0.02, 0.2, 8, 1)
        glPopMatrix()
        
        glColor3f(0.0, 0.8, 0.0)
        for angulo in [0, 90, 180, 270]:
            glPushMatrix()
            glTranslatef(0, 0.1, 0)
            glRotatef(angulo, 0, 1, 0)
            glRotatef(45, 1, 0, 0)
            glScalef(0.1, 0.1, 0.2)
            quad = gluNewQuadric()
            gluSphere(quad, 0.5, 8, 8)
            glPopMatrix()
        
        glPopMatrix()
        