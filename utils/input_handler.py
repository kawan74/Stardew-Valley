import glfw

# Velocidade do movimento
movement_speed = 0.05

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