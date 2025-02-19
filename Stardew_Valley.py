from OpenGL.GL import *
from OpenGL.GLU import *
import glfw
import time

# Configurações da câmera
camera_pos = [0, 0, -3]
camera_angle = 0
last_time = time.time()

# Velocidade da câmera
smooth_speed = 0.3
rotation_speed = 50.0

# Modo da câmera (3D ou 2D)
modo_camera = '3D'

def init_window(width, height, title):
    if not glfw.init(): 
        return None
    
    window = glfw.create_window(width, height, title, None, None)
    if not window:
        glfw.terminate()
        return None
    
    glfw.make_context_current(window)
    return window

def configurar_camera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    if modo_camera == '3D':
        gluPerspective(100, 1.0, 0.1, 100)
    else:
        glOrtho(-7, 7, -7, 7, -15, 10)  
    glMatrixMode(GL_MODELVIEW)

def configurar_cenario():
    glClearColor(0.5, 0.8, 1.0, 1.0) if modo_camera == '2D' else glClearColor(0.1, 0.1, 0.3, 1.0)
    
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)  
    
    # Posição da luz: mais para frente e para o alto
    glLightfv(GL_LIGHT0, GL_POSITION, [1, 3, 2, 1])  
    
    # Intensidade da luz difusa 
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1, 1, 1, 1])  
    
    # Luz ambiente mais forte para evitar escuridão total
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.3, 0.3, 0.3, 1])
    
    glEnable(GL_DEPTH_TEST)  


def iniciar_opengl():
    configurar_cenario()
    glEnable(GL_DEPTH_TEST)
    configurar_camera()

def desenhar_chao():
    glColor3f(0.1, 0.7, 0.1)  
    glBegin(GL_QUADS)
    
    if modo_camera == '3D':
        glVertex3f(-5, -1, -5)
        glVertex3f(5, -1, -5)
        glVertex3f(5, -1, 5)
        glVertex3f(-5, -1, 5)
    else:  # Ajuste para 2D
        glVertex2f(-7, -7)
        glVertex2f(7, -7)
        glVertex2f(7, -3)
        glVertex2f(-7, -3)
    
    glEnd()

def desenhar_casa():
    glDisable(GL_LIGHTING)  
    glColor3f(0.8, 0.5, 0.2)  
    glBegin(GL_QUADS)
    
    if modo_camera == '3D':
        glVertex3f(-0.3, -1, 0.0)
        glVertex3f(-0.3, -0.6, 0.0)
        glVertex3f(0.3, -0.6, 0.0)
        glVertex3f(0.3, -1, 0.0)
    else:  # Ajuste para 2D
        glVertex2f(-0.5, -3.0)  
        glVertex2f(-0.5, -2.0)  
        glVertex2f(0.5, -2.0)
        glVertex2f(0.5, -3.0)
    
    glEnd()
    
    glColor3f(0.7, 0.1, 0.1)  
    glBegin(GL_TRIANGLES)
    
    if modo_camera == '3D':
        glVertex3f(-0.35, -0.6, 0.0)
        glVertex3f(0.35, -0.6, 0.0)
        glVertex3f(0.0, -0.3, 0.0)
    else:  # Ajuste para 2D
        glVertex2f(-0.55, -2.0)
        glVertex2f(0.55, -2.0)
        glVertex2f(0.0, -1.5)  
        
    glEnd() 


def desenhar_cenario():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    if modo_camera == '3D':
        glTranslatef(camera_pos[0], camera_pos[1], camera_pos[2])
        glRotatef(camera_angle, 0, 1, 0)
        desenhar_chao()
        desenhar_casa()
    else:
        glTranslatef(0, -3, 0)
        desenhar_chao()
        desenhar_casa()


def process_input(window):
    global camera_pos, camera_angle, last_time, modo_camera
    
    delta_time = time.time() - last_time
    last_time = time.time()
    move_speed = smooth_speed * delta_time
    
    if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS and modo_camera == '3D':
        camera_pos[2] += move_speed
    if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS and modo_camera == '3D':
        camera_pos[2] -= move_speed
    if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS and modo_camera == '3D':
        camera_pos[0] -= move_speed
    if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS and modo_camera == '3D':
        camera_pos[0] += move_speed
    
    if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS and modo_camera == '3D':
        camera_angle -= rotation_speed * delta_time
    if glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS and modo_camera == '3D':
        camera_angle += rotation_speed * delta_time
    
    if glfw.get_key(window, glfw.KEY_SPACE) == glfw.PRESS:
        modo_camera = '2D' if modo_camera == '3D' else '3D'
        configurar_camera()
        configurar_cenario()

def main():
    window = init_window(800, 800, 'Jogo')
    if not window:
        return
    
    iniciar_opengl()
    
    while not glfw.window_should_close(window):
        glfw.poll_events()
        process_input(window)
        desenhar_cenario()
        glfw.swap_buffers(window)
    
    glfw.terminate()

if __name__ == '__main__':  
    main()
