import glfw
from OpenGL.GL import *

def inicio():
    glClearColor(1,1,1,1)

def cerca():
    verticesCercaPe1 = [
        [-0.1,-0.1],
        [-0.1,0.3],
        [0.0,0.3],
        [0.0,-0.1]
    ]

    glColor3f(128/255, 59/255, 18/255)
    glBegin(GL_QUADS)
    for v in verticesCercaPe1:
        glVertex2fv(v)
    glEnd()

    verticesCercaDeitado1 = [
        [-0.1, 0.125],
        [-0.1, 0.2],
        [0.15, 0.2],
        [0.15, 0.125]
    ]

    glPushMatrix()
    glColor3f(128/255, 59/255, 18/255)
    glBegin(GL_QUADS)
    for v in verticesCercaDeitado1:
        glVertex2fv(v)
    glEnd()
    glPopMatrix()

    verticesCercaDeitado2 = [
        [-0.1, 0.0],
        [-0.1, 0.075],
        [0.15, 0.075],
        [0.15, 0.0]
    ]
    
    glPushMatrix()
    glColor3f(128/255, 59/255, 18/255)
    glBegin(GL_QUADS)
    for v in verticesCercaDeitado2:
        glVertex2fv(v)
    glEnd()
    glPopMatrix()

    verticesCercaPe2 = [
        [0.15,-0.1],
        [0.15,0.3],
        [0.25,0.3],
        [0.25,-0.1]
    ]

    glPushMatrix()
    glColor3f(128/255, 59/255, 18/255)
    glBegin(GL_QUADS)
    for v in verticesCercaPe2:
        glVertex2fv(v)
    glEnd()
    glPopMatrix()

def render():
    glClear(GL_COLOR_BUFFER_BIT)
    cerca()

def main():
    glfw.init()                                                      
    window = glfw.create_window(500,500,'Stardew Valley',None,None)
    glfw.make_context_current(window)                               
    inicio()                                                    
    while not glfw.window_should_close(window):                     
        glfw.poll_events()                                          
        render()                                                    
        glfw.swap_buffers(window)                                   
    glfw.terminate()                                                

if __name__ == '__main__':
    main()