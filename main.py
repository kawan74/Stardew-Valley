import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from render import render_scene 

# Variáveis globais para a posição do personagem
character_position = [0.0, 0.0]  # Posição inicial do personagem
movement_speed = 0.1  # Velocidade de movimento

# Função de callback para o tratamento das teclas pressionadas
def key_callback(window, key, scancode, action, mods):
    global character_position

    min_x, max_x = -1.0, 1.0
    min_y, max_y = -1.3, 0.2

    if action == glfw.PRESS or action == glfw.REPEAT:
        new_x, new_y = character_position[0], character_position[1]

        if key == glfw.KEY_W:  # Move para cima
            new_y += movement_speed
        elif key == glfw.KEY_S:  # Move para baixo
            new_y -= movement_speed
        elif key == glfw.KEY_A:  # Move para a esquerda
            new_x -= movement_speed
        elif key == glfw.KEY_D:  # Move para a direita
            new_x += movement_speed

        # Verifica se a nova posição está dentro dos limites
        if min_x <= new_x <= max_x and min_y <= new_y <= max_y:
            character_position[0], character_position[1] = new_x, new_y

# Função para inicializar a janela com glfw
def init_window():
    if not glfw.init():
        raise Exception("GLFW can't be initialized")
    
    # Criação da janela com tamanho e título
    window = glfw.create_window(800, 600, "Meu Jogo", None, None)
    
    if not window:
        glfw.terminate()
        raise Exception("GLFW window can't be created")
    
    glfw.make_context_current(window)

    # Configura o callback de teclas
    glfw.set_key_callback(window, key_callback)

    return window

# Função para configurar o fundo
def setup_background():
    glClearColor(0.5, 0.8, 1.0, 1.0)  # Cor do fundo (céu)

# Função principal
def main():
    window = init_window()  # Criação da janela
    
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)  # Limpa a tela
        setup_background()  # Configura o fundo
        
        # Renderiza a cena
        render_scene()  # Renderiza os objetos da cena
        
        glfw.swap_buffers(window)  # Troca os buffers da janela
        glfw.poll_events()  # Atualiza eventos (entrada de usuário, etc.)

    glfw.terminate()  # Termina o uso do GLFW ao fechar a janela

# Chama a função principal
if __name__ == "__main__":
    main()
