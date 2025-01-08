import glfw
from OpenGL.GL import *

def setup_background():
    glClearColor(0.5, 0.8, 1.0, 1.0) #ceu

def draw_fence():
    glColor3f(0.5, 0.3, 0.1)  #vertical
    for i in range(-5, 6):
        x = i * 0.1
        vertices = [
            [x - 0.02, -0.2],
            [x - 0.02, 0.1],
            [x + 0.02, 0.1],
            [x + 0.02, -0.2]
        ]
        glBegin(GL_QUADS)
        for vertex in vertices:
            glVertex2fv(vertex)
        glEnd()

    glColor3f(0.6, 0.4, 0.2)  #horizontal
    for y_offset in [-0.05, 0.05]:
        vertices = [
            [-0.6, y_offset - 0.01],
            [-0.6, y_offset + 0.01],
            [0.6, y_offset + 0.01],
            [0.6, y_offset - 0.01]
        ]
        glBegin(GL_QUADS)
        for vertex in vertices:
            glVertex2fv(vertex)
        glEnd()

def draw_house():
    glColor3f(0.9, 0.6, 0.3)  #casa
    body_vertices = [
        [-0.3, -0.2],
        [-0.3, 0.2],
        [0.3, 0.2],
        [0.3, -0.2]
    ]
    glBegin(GL_QUADS)
    for vertex in body_vertices:
        glVertex2fv(vertex)
    glEnd()

    #telhado
    glColor3f(0.7, 0.1, 0.1) 
    roof_vertices = [
        [-0.4, 0.2],
        [0.4, 0.2],
        [0.0, 0.5]
    ]
    glBegin(GL_TRIANGLES)
    for vertex in roof_vertices:
        glVertex2fv(vertex)
    glEnd()

    #porta
    glColor3f(0.5, 0.3, 0.1)  
    door_vertices = [
        [-0.05, -0.2],
        [-0.05, 0.05],
        [0.05, 0.05],
        [0.05, -0.2]
    ]
    glBegin(GL_QUADS)
    for vertex in door_vertices:
        glVertex2fv(vertex)
    glEnd()

    #janela
    glColor3f(0.7, 0.9, 1.0)  
    window_vertices = [
        [[-0.25, 0.0], [-0.15, 0.0], [-0.15, 0.1], [-0.25, 0.1]],
        [[0.15, 0.0], [0.25, 0.0], [0.25, 0.1], [0.15, 0.1]]
    ]
    for vertices in window_vertices:
        glBegin(GL_QUADS)
        for vertex in vertices:
            glVertex2fv(vertex)
        glEnd()

def draw_grass():
    glColor3f(0.3, 0.7, 0.2)  #grama
    grass_vertices = [
        [-1.0, -0.5],
        [-1.0, -0.2],
        [1.0, -0.2],
        [1.0, -0.5]
    ]
    glBegin(GL_QUADS)
    for vertex in grass_vertices:
        glVertex2fv(vertex)
    glEnd()

def render_scene():
    glClear(GL_COLOR_BUFFER_BIT)
    draw_grass()
    draw_house()
    draw_fence()

def main():
    if not glfw.init():
        return

    window = glfw.create_window(500, 500, "Stardew Valley", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    setup_background()

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render_scene()
        glfw.swap_buffers(window)

    glfw.terminate() 


if __name__ == "__main__":
    main()
    