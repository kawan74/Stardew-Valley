import glfw
from OpenGL.GL import *

def inicio():
    glClearColor(1,1,1,1)

def cerca():
    verticesCercaPE = [
        [-0.1,0.0],
        [-0.1,0.3],
        [0.0,0.3],
        [0.0,0.0]
    ]

    glColor3f(128/255, 59/255, 18/255)
    glBegin(GL_QUADS)
    for v in verticesCercaPE:
        glVertex2fv(v)
    glEnd()

    verticesCercaDeitado = [
        []
    ]

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