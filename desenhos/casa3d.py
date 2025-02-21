from OpenGL.GL import *
from OpenGL.GLU import *
import glfw

def initialize():
    glClearColor(1, 1, 1, 1)
    glEnable(GL_DEPTH_TEST)  # Ativar o z-buffer

def casa():
    # Corpo da casa
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

def render():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1, 0.1, 50)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(2, 2, 2, 0, 0.2, 0, 0, 1, 0)
    
    glPushMatrix()
    glRotatef(225,0,1,0)
    glTranslatef(0, -0.2, 0)
    casa()
    glPopMatrix()

def main():
    if not glfw.init():
        return
    window = glfw.create_window(800, 800, "Casa 3D", None, None)
    glfw.make_context_current(window)
    initialize()
    
    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)
    
    glfw.terminate()

if __name__ == "__main__":
    main()