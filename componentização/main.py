from game import JogoOpenGL

if __name__ == '__main__':
    jogo = JogoOpenGL()
    
    # Plantação de tomates
    linhas = 5
    colunas = 8
    espacamento = 1.0
    
    inicio_x = -4
    inicio_z = -4
    
    # Criar grade de plantas de tomate
    for linha in range(linhas):
        for coluna in range(colunas):
            x = inicio_x + (coluna * espacamento)
            z = inicio_z + (linha * espacamento)
            jogo.adicionar_planta("tomate", x, z)
    
    # Flores roxas nas bordas da plantação
    for i in range(linhas):
        jogo.adicionar_planta("flor", inicio_x - espacamento, inicio_z + (i * espacamento))
        jogo.adicionar_planta("flor", inicio_x + (colunas * espacamento), inicio_z + (i * espacamento))
    
    # Flores roxas na frente da casa
    for x in range(-2, 3):  # 5 flores na frente da casa
        jogo.adicionar_planta("flor", x, 2)  # Ajuste o Z (2) conforme necessário
    
    jogo.executar()