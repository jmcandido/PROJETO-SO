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

def imprimir_tabela_FCFS(tempoChegadas, tempoEsperaLista, tempoRespostaLista, tempoRetornoLista):
    quantidadeProcessos = len(tempoChegadas)
    
    for i in range(quantidadeProcessos):
        tempoMedioEspera = sum(tempoEsperaLista) / quantidadeProcessos
        tempoMedioRetorno = sum(tempoRetornoLista) / quantidadeProcessos
        tempoMedioResposta = sum(tempoRespostaLista) / quantidadeProcessos
    

    print("FCFS: {:.1f} {:.1f} {:.1f}".format(tempoMedioRetorno, tempoMedioResposta, tempoMedioEspera))

def imprimir_tabela_SJF(tempoChegadas, tempoEsperaLista, tempoRespostaLista, tempoRetornoLista):
    quantidadeProcessos = len(tempoChegadas)
    
    for i in range(quantidadeProcessos):
        tempoMedioEspera = sum(tempoEsperaLista) / quantidadeProcessos
        tempoMedioRetorno = sum(tempoRetornoLista) / quantidadeProcessos
        tempoMedioResposta = sum(tempoRespostaLista) / quantidadeProcessos
    

    print("SJF: {:.1f} {:.1f} {:.1f}".format(tempoMedioRetorno, tempoMedioResposta, tempoMedioEspera))

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
    imprimir_tabela_FCFS(tempoChegadas, tempoEsperaLista, tempoRespostaLista, tempoRetornoLista)

def SJF(tempos_chegada, picos_cpu):
    
    processos = list(zip(tempos_chegada, picos_cpu))
    processos.sort(key=lambda x: (x[0], x[1]))  # Ordena por tempo de chegada e depois por tempo de execução
    
    schedule = []  # Lista de tempos de início
    tempo_atual = 0  # Tempo atual do sistema
    fila = []  # Fila de processos disponíveis
    indice = 0  # Índice para percorrer a lista de processos
    num_processos = len(processos)
    
    tempos_retorno = []
    tempos_resposta = []
    tempos_espera = []
    
    while indice < num_processos or fila:
        # Adicionar processos à fila quando chegarem
        while indice < num_processos and processos[indice][0] <= tempo_atual:
            fila.append(processos[indice])
            indice += 1
        
        if fila:
            fila.sort(key=lambda x: x[1])  # Ordena por menor tempo de execução
            proximo_processo = fila.pop(0)  # Pega o processo com menor tempo de execução
            tempo_inicio = tempo_atual  # Momento em que o processo começa a execução
            tempo_termino = tempo_inicio + proximo_processo[1]
            
            schedule.append((proximo_processo[0], tempo_inicio))  # Registra o início
            tempo_atual = tempo_termino  # Atualiza o tempo atual
            
            # Cálculo das métricas
            tempo_retorno = tempo_termino - proximo_processo[0]
            tempo_resposta = tempo_inicio - proximo_processo[0]
            tempo_espera = tempo_resposta  # Para SJF sem preempção, espera = resposta
            
            tempos_retorno.append(tempo_retorno)
            tempos_resposta.append(tempo_resposta)
            tempos_espera.append(tempo_espera)
        else:
            tempo_atual = processos[indice][0]  # Avança para o próximo processo se a fila estiver vazia
    
    imprimir_tabela_SJF(tempos_chegada, tempos_espera, tempos_resposta, tempos_retorno)

arquivo = "testes.txt"
tempoChegadas, tempoPicos = ler_arquivo(arquivo)
FCFS(tempoChegadas, tempoPicos)
SJF(tempoChegadas, tempoPicos)

