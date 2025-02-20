from OpenGL.GL import *
from OpenGL.GLU import *
import glfw

def initialize():
    glClearColor(0.5, 0.5, 0.5, 1)
    glEnable(GL_DEPTH_TEST)

def galinha():
    # Corpo da galinha (paralelepípedo branco)
    glColor3f(1.0, 1.0, 1.0)
    body_vertices = [
        [-0.2, 0.0, -0.2], [0.2, 0.0, -0.2], [0.2, 0.4, -0.2], [-0.2, 0.4, -0.2],
        [-0.2, 0.0, 0.2], [0.2, 0.0, 0.2], [0.2, 0.4, 0.2], [-0.2, 0.4, 0.2]
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
    
    # Crista da galinha (paralelepípedo vermelho - largura igual à cabeça)
    glColor3f(1.0, 0.0, 0.0)
    crest_vertices = [
        [-0.2, 0.4, -0.05], [0.2, 0.4, -0.05], [0.2, 0.5, -0.05], [-0.2, 0.5, -0.05],
        [-0.2, 0.4, 0.05], [0.2, 0.4, 0.05], [0.2, 0.5, 0.05], [-0.2, 0.5, 0.05]
    ]
    glBegin(GL_QUADS)
    for f in faces:
        for vertex in f:
            glVertex3fv(crest_vertices[vertex])
    glEnd()
    
    # Bico da galinha (paralelepípedo amarelo mais à frente)
    glColor3f(1.0, 1.0, 0.0)
    beak_vertices = [
        [0.1, 0.15, -0.25], [0.2, 0.15, -0.25], [0.2, 0.25, -0.25], [0.1, 0.25, -0.25]
    ]
    glBegin(GL_QUADS)
    for vertex in beak_vertices:
        glVertex3fv(vertex)
    glEnd()
    
    # Olhos da galinha (pequenos paralelepípedos pretos)
    glColor3f(0.0, 0.0, 0.0)
    eye_vertices = [
        [[-0.1, 0.3, -0.21], [-0.05, 0.3, -0.21], [-0.05, 0.35, -0.21], [-0.1, 0.35, -0.21]],
        [[0.05, 0.3, -0.21], [0.1, 0.3, -0.21], [0.1, 0.35, -0.21], [0.05, 0.35, -0.21]]
    ]
    for eye in eye_vertices:
        glBegin(GL_QUADS)
        for vertex in eye:
            glVertex3fv(vertex)
        glEnd()
    
    # Pernas da galinha (paralelepípedos pretos)
    glColor3f(0.0, 0.0, 0.0)
    leg_vertices = [
        [[-0.1, -0.2, -0.05], [-0.05, -0.2, -0.05], [-0.05, 0.0, -0.05], [-0.1, 0.0, -0.05],
         [-0.1, -0.2, 0.05], [-0.05, -0.2, 0.05], [-0.05, 0.0, 0.05], [-0.1, 0.0, 0.05]],
        [[0.05, -0.2, -0.05], [0.1, -0.2, -0.05], [0.1, 0.0, -0.05], [0.05, 0.0, -0.05],
         [0.05, -0.2, 0.05], [0.1, -0.2, 0.05], [0.1, 0.0, 0.05], [0.05, 0.0, 0.05]]
    ]
    for leg in leg_vertices:
        glBegin(GL_QUADS)
        for f in faces:
            for vertex in f:
                glVertex3fv(leg[vertex])
        glEnd()

def render():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1, 0.1, 50)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(2, 2, 2, 0, 0.2, 0, 0, 1, 0)
    
    glPushMatrix()
    glRotatef(180, 0, 1, 0)
    glTranslatef(0, -0.2, 0)
    galinha()
    glPopMatrix()

def main():
    if not glfw.init():
        return
    window = glfw.create_window(800, 800, "Galinha 3D", None, None)
    glfw.make_context_current(window)
    initialize()
    
    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)
    
    glfw.terminate()

if __name__ == "__main__":
    main()