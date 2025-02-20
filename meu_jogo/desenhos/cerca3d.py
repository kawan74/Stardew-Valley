from OpenGL.GL import *
from OpenGL.GLU import *
import glfw

def initialize():
    glClearColor(1, 1, 1, 1)
    glEnable(GL_DEPTH_TEST)

def cerca():
    glColor3f(0.5, 0.3, 0.1)  # Cor marrom para os postes
    post_positions = [-0.1, 0.1]
    for x in post_positions:
        vertices = [
            [x - 0.01, -0.2, -0.01], [x + 0.01, -0.2, -0.01], [x + 0.01, 0.1, -0.01], [x - 0.01, 0.1, -0.01],
            [x - 0.01, -0.2, 0.01], [x + 0.01, -0.2, 0.01], [x + 0.01, 0.1, 0.01], [x - 0.01, 0.1, 0.01]
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
    for y_offset in [-0.05, 0.05]:
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

def render():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1, 0.1, 50)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(2, 2, 2, 0, 0.2, 0, 0, 1, 0)

    
    glPushMatrix()
    glTranslatef(-1, -0.2, 0)
    cerca()
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
