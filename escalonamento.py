def ler_arquivo(nome_arquivo):

    """Lê os tempos de chegada e execução do arquivo."""
    tempoChegadas = []
    tempoPicos = []
    
    with open(nome_arquivo, "r") as file:
        for linha in file:
            chegada, pico = map(int, linha.split())
            tempoChegadas.append(chegada)
            tempoPicos.append(pico)
    
    return tempoChegadas, tempoPicos

def imprimir_tabela_final(tempoChegadas, tempoEsperaLista, tempoRespostaLista, tempoRetornoLista):
    quantidadeProcessos = len(tempoChegadas)
    
    for i in range(quantidadeProcessos):
        tempoMedioEspera = sum(tempoEsperaLista) / quantidadeProcessos
        tempoMedioRetorno = sum(tempoRetornoLista) / quantidadeProcessos
        tempoMedioResposta = sum(tempoRespostaLista) / quantidadeProcessos
    

    print("FCFCS: {:.1f} {:.1f} {:.1f}".format(tempoMedioRetorno, tempoMedioResposta, tempoMedioEspera))

def FCFS(tempoChegadas, tempoPicos):
    quantidadeProcessos = len(tempoChegadas)
    
    processos = list(zip(tempoChegadas, tempoPicos))
    
    # Ordena os processos por tempo de chegada (caso não estejam ordenados)
    processos.sort(key=lambda x: x[0])


    tempoAtual = 0
    inicioExecucao = []
    fimExecucao = []

    tempoEsperaLista = []
    tempoRetornoLista = []
    tempoRespostaLista = []

    # Loop para execução dos processos
    for chegada, pico in processos:
        if tempoAtual < chegada:
            tempoAtual = chegada  # Avança o tempo para quando o processo chega
        
        inicioExecucao.append(tempoAtual)  # O processo começa no tempoAtual ou quando chega
        tempoAtual += pico  # Adiciona o tempo de execução do processo
        fimExecucao.append(tempoAtual)  # O tempo final é o tempoAtual somado ao tempo de execução

    # Calculando tempos individuais
    for i in range(quantidadeProcessos):
        tempoRetorno = fimExecucao[i] - tempoChegadas[i]
        tempoResposta = tempoEspera = inicioExecucao[i] - tempoChegadas[i]
        
        tempoRetornoLista.append(tempoRetorno)
        tempoRespostaLista.append(tempoResposta)
        tempoEsperaLista.append(tempoEspera)


    # Chama a função que imprime os resultados
    imprimir_tabela_final(tempoChegadas, tempoEsperaLista, tempoRespostaLista, tempoRetornoLista)

arquivo = "testes.txt"
tempoChegadas, tempoPicos = ler_arquivo(arquivo)
FCFS(tempoChegadas, tempoPicos)


