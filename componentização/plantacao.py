def adicionar_plantas(jogo):
    linhas = 5
    colunas = 8
    espacamento = 1.0
    
    inicio_x = -4
    inicio_z = -4

    for linha in range(linhas):
        for coluna in range(colunas):
            x = inicio_x + (coluna * espacamento)
            z = inicio_z + (linha * espacamento)
            jogo.adicionar_planta("tomate", x, z)

    for i in range(linhas):
        jogo.adicionar_planta("flor", inicio_x - espacamento, inicio_z + (i * espacamento))
        jogo.adicionar_planta("flor", inicio_x + (colunas * espacamento), inicio_z + (i * espacamento))
    
    for x in range(-2, 3):  
        jogo.adicionar_planta("flor", x, 2) 