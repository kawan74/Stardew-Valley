import glfw

def iniciar_janela(largura, altura, titulo, camera):
    if not glfw.init():
        return None

    window = glfw.create_window(largura, altura, titulo, None, None)
    if not window:
        glfw.terminate()
        return None

    glfw.make_context_current(window)
    glfw.set_cursor_pos_callback(window, camera.mouse_callback)
    glfw.set_key_callback(window, camera.teclado_callback)
    return window
