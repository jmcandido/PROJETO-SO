def ler_arquivo(nome_arquivo):

    tempoChegadas = []
    tempoPicos = []
    
    with open(nome_arquivo, "r") as file:
        for linha in file:
            chegada, pico = map(int, linha.split())
            tempoChegadas.append(chegada)
            tempoPicos.append(pico)
    
    return tempoChegadas, tempoPicos

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
        tempoEspera = tempoRetorno - tempoPicos[i]
        tempoResposta = inicioExecucao[i] - tempoChegadas[i]
        
        tempoRetornoLista.append(tempoRetorno)
        tempoRespostaLista.append(tempoResposta)
        tempoEsperaLista.append(tempoEspera)


    # Chama a função que imprime os resultados
    imprimir_tabela_final(tempoChegadas, tempoEsperaLista, tempoRespostaLista, tempoRetornoLista,0)

def SJF(tempoChegadas, tempoPicos):
    
    quantidadeProcessos = len(tempoChegadas)
    processos = list(zip(tempoChegadas, tempoPicos))
    
    # Ordena inicialmente os processos pelo tempo de chegada
    processos.sort(key=lambda x: x[0])

    tempoAtual = 0
    inicioExecucao = []
    fimExecucao = []
    tempoEsperaLista = []
    tempoRetornoLista = []
    tempoRespostaLista = []

    processos_prontos = []
    processos_restantes = processos.copy()

    while processos_restantes or processos_prontos:
        # Adicionar à fila de prontos os processos que já chegaram
        while processos_restantes and processos_restantes[0][0] <= tempoAtual:
            processos_prontos.append(processos_restantes.pop(0))

        # Se não há processos prontos, avançar no tempo
        if not (processos_prontos):
            tempoAtual = processos_restantes[0][0]
            continue

        # Escolher o processo com o menor tempo de execução
        processos_prontos.sort(key=lambda x: x[1])
        chegada, pico = processos_prontos.pop(0)

        inicioExecucao.append(tempoAtual)
        tempoAtual += pico
        fimExecucao.append(tempoAtual)
        
    # Calculando tempos individuais
    for i in range(quantidadeProcessos):
        tempoRetorno = fimExecucao[i] - tempoChegadas[i]
        tempoEspera = tempoRetorno - tempoPicos[i]
        tempoResposta = inicioExecucao[i] - tempoChegadas[i]
        
        tempoRetornoLista.append(tempoRetorno)
        tempoRespostaLista.append(tempoResposta)
        tempoEsperaLista.append(tempoEspera)

    # Função de impressão de tabela
    imprimir_tabela_final(tempoChegadas, tempoEsperaLista, tempoRespostaLista, tempoRetornoLista, 1)

def imprimir_tabela_final(tempoChegadas, tempoEsperaLista, tempoRespostaLista, tempoRetornoLista, id):
    quantidadeProcessos = len(tempoChegadas)
    
    for i in range(quantidadeProcessos):
        tempoMedioEspera = sum(tempoEsperaLista) / quantidadeProcessos
        tempoMedioRetorno = sum(tempoRetornoLista) / quantidadeProcessos
        tempoMedioResposta = sum(tempoRespostaLista) / quantidadeProcessos

    
    if (id == 0):
         print("FCFS: {:.1f} {:.1f} {:.1f}".format(tempoMedioRetorno, tempoMedioResposta, tempoMedioEspera))
    elif(id == 1):
        print("SJF: {:.1f} {:.1f} {:.1f}".format(tempoMedioRetorno, tempoMedioResposta, tempoMedioEspera))


arquivo = "testes.txt"
tempoChegadas, tempoPicos = ler_arquivo(arquivo)
FCFS(tempoChegadas, tempoPicos)
SJF(tempoChegadas,tempoPicos)



