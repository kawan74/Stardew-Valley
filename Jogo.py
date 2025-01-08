import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np

# Vertex Shader
VERTEX_SHADER = """
#version 330 core
layout(location = 0) in vec3 position;
layout(location = 1) in vec3 color;

out vec3 fragColor;

void main() {
    gl_Position = vec4(position, 1.0);
    fragColor = color;
}
"""

# Fragment Shader
FRAGMENT_SHADER = """
#version 330 core
in vec3 fragColor;

out vec4 fragColorOut;

void main() {
    fragColorOut = vec4(fragColor, 1.0);
}
"""

def main():
   
    if not glfw.init():
        return

    # Configuração da janela
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    window = glfw.create_window(800, 600, "Cenário Inicial", None, None)

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    # Compilação dos shaders
    shader = compileProgram(
        compileShader(VERTEX_SHADER, GL_VERTEX_SHADER),
        compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER)
    )

    # Dados para o cenário e a casinha
    vertices = [
        # Posição          # Cor (RGB)

        # Céu
        -1.0,  0.0, 0.0,   0.53, 0.81, 0.98,  # Inferior esquerdo
         1.0,  0.0, 0.0,   0.53, 0.81, 0.98,  # Inferior direito
         1.0,  1.0, 0.0,   0.53, 0.81, 0.98,  # Superior direito
        -1.0,  1.0, 0.0,   0.53, 0.81, 0.98,  # Superior esquerdo

        # Chão
        -1.0, -1.0, 0.0,   0.13, 0.55, 0.13,  # Inferior esquerdo
         1.0, -1.0, 0.0,   0.13, 0.55, 0.13,  # Inferior direito
         1.0,  0.0, 0.0,   0.13, 0.55, 0.13,  # Superior direito
        -1.0,  0.0, 0.0,   0.13, 0.55, 0.13,  # Superior esquerdo

        # Base da casa
        -0.6, -0.3, 0.0,   0.87, 0.72, 0.53,  # Inferior esquerdo (marrom claro)
        -0.2, -0.3, 0.0,   0.87, 0.72, 0.53,  # Inferior direito
        -0.2,  0.1, 0.0,   0.87, 0.72, 0.53,  # Superior direito
        -0.6,  0.1, 0.0,   0.87, 0.72, 0.53,  # Superior esquerdo

        # Telhado da casa
        -0.65,  0.1, 0.0,   0.55, 0.27, 0.07,  # Esquerdo (marrom escuro)
        -0.15,  0.1, 0.0,   0.55, 0.27, 0.07,  # Direito
        -0.4,   0.4, 0.0,   0.55, 0.27, 0.07,  # Superior (ponta do triângulo)

        # Porta
        -0.5, -0.3, 0.0,   0.36, 0.25, 0.20,  # Inferior esquerdo (marrom)
        -0.35, -0.3, 0.0,  0.36, 0.25, 0.20,  # Inferior direito
        -0.35,  0.0, 0.0,  0.36, 0.25, 0.20,  # Superior direito
        -0.5,   0.0, 0.0,  0.36, 0.25, 0.20,  # Superior esquerdo

        # Janela
        -0.3, -0.15, 0.0,  0.68, 0.85, 0.90,  # Inferior esquerdo (azul claro)
        -0.2, -0.15, 0.0,  0.68, 0.85, 0.90,  # Inferior direito
        -0.2, -0.05, 0.0,  0.68, 0.85, 0.90,  # Superior direito
        -0.3, -0.05, 0.0,  0.68, 0.85, 0.90   # Superior esquerdo
    ]
    vertices = np.array(vertices, dtype=np.float32)

    indices = [
        # Céu
        0, 1, 2, 2, 3, 0,

        # Chão
        4, 5, 6, 6, 7, 4,

        # Base da casa
        8, 9, 10, 10, 11, 8,

        # Telhado
        12, 13, 14,

        # Porta
        15, 16, 17, 17, 18, 15,

        # Janela
        19, 20, 21, 21, 22, 19
    ]
    indices = np.array(indices, dtype=np.uint32)

    # Configuração do VAO e VBO
    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)
    EBO = glGenBuffers(1)

    glBindVertexArray(VAO)

    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

    # Posição
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * 4, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    # Cor
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * 4, ctypes.c_void_p(12))
    glEnableVertexAttribArray(1)

    # Loop principal
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)

        # Usar o shader
        glUseProgram(shader)

        # Desenhar o cenário
        glBindVertexArray(VAO)
        glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)

        glfw.swap_buffers(window)
        glfw.poll_events()

    # Cleanup
    glfw.terminate()


if __name__ == "__main__":
    main()
