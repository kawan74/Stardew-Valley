from OpenGL.GL import *
from OpenGL.GLU import *
import glfw

def initialize():
    glClearColor(0.5, 0.5, 0.5, 1)
    glEnable(GL_DEPTH_TEST)

def planta():
    # Tronco da planta (cilindro verde)
    glColor3f(0.0, 0.5, 0.0)
    glBegin(GL_QUADS)
    for vertex in [[-0.02, 0.0, -0.02], [0.02, 0.0, -0.02], [0.02, 0.3, -0.02], [-0.02, 0.3, -0.02],
                   [-0.02, 0.0, 0.02], [0.02, 0.0, 0.02], [0.02, 0.3, 0.02], [-0.02, 0.3, 0.02]]:
        glVertex3fv(vertex)
    glEnd()
    
    # Flor (esfera azul no topo)
    glColor3f(0.0, 0.0, 1.0)
    glPushMatrix()
    glTranslatef(0, 0.35, 0)
    quad = gluNewQuadric()
    gluSphere(quad, 0.1, 16, 16)
    glPopMatrix()

def render():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1, 0.1, 50)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(2, 2, 2, 0, 0.2, 0, 0, 1, 0)
    
    glPushMatrix()
    planta()
    glPopMatrix()

def main():
    if not glfw.init():
        return
    window = glfw.create_window(800, 800, "Cena 3D", None, None)
    glfw.make_context_current(window)
    initialize()
    
    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)
    
    glfw.terminate()

if __name__ == "__main__":
    main()
