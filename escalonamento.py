from collections import deque
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

def RR(tempos_chegada, tempos_execucao, quantum):
    #Cria um lista de tuplas com os processos,porém com um ID,esse ID tem o msm tamanho da qtd de processos
    processos = [(i + 1, tempos_chegada[i], tempos_execucao[i]) for i in range(len(tempos_chegada))]
    #i+1 é apenas para o ID inicar em 1
    
    #Ordena os processos por tempo de chegada usando TimSort, que é um algoritmo híbrido derivado do merge sort e do insertion sort usado no Python
    processos.sort(key=lambda x: x[1])  # Ordenação pelo tempo de chegada
    
    fila = deque()
    tempo_atual = 0
    indice_processo = 0
    tempos_retorno = {}  # Tempo de retorno de cada processo
    tempos_resposta = {}  # Tempo de resposta de cada processo
    execucoes = {}  # Momento da primeira execução de cada processo
    tempos_espera = {p[0]: 0 for p in processos}  # Tempo de espera de cada processo

    while fila or indice_processo < len(processos):
        #Primeiro While verifica e garante que todos os processos que chegam em 0 sejam adicionados a fila
        while indice_processo < len(processos) and processos[indice_processo][1] <= tempo_atual:#Se o index é menor que o tam da lista e o processo[index][tempo de chegada]< tempo atual, adiciona na fila
            fila.append([processos[indice_processo][0], processos[indice_processo][2], processos[indice_processo][1]])  # (ID, Tempo Restante, Tempo Chegada)
            indice_processo += 1
        
        if fila:
            id_processo, tempo_restante, tempo_chegada = fila.popleft()
            #Se o id do processo que estou não está em execucoes, então é a primeira vez que ele está sendo executado
            if id_processo not in execucoes:
                tempos_resposta[id_processo] = tempo_atual - tempo_chegada  # Tempo da primeira execução
                execucoes[id_processo] = tempo_atual
            
            #Tempo que passa executando é o min entre o quantum e o tempo restante
            tempo_execucao = min(quantum, tempo_restante)
            tempo_atual += tempo_execucao

            #Segundo While verifica se há processos que chegaram enquanto um processo está sendo executado
            while indice_processo < len(processos) and processos[indice_processo][1] <= tempo_atual:
                fila.append([processos[indice_processo][0], processos[indice_processo][2], processos[indice_processo][1]])
                indice_processo += 1
            
            #Verifica se o tempo restante do processo é maior que o quantum,caso seja, retorna pra fila
            if tempo_restante > quantum:
                fila.append([id_processo, tempo_restante - quantum, tempo_chegada])#Passa para fila porém atualizando o tempo restante
            else:
                tempos_retorno[id_processo] = tempo_atual - tempo_chegada  # Tempo de retorno

        else:# Se a fila estiver vazia, incrementa o tempo atual
            tempo_atual += 1

    # Cálculo dos tempos de espera
    for id_processo in tempos_retorno:
        tempo_pico = [p[2] for p in processos if p[0] == id_processo][0]  
        tempos_espera[id_processo] = tempos_retorno[id_processo] - tempo_pico

    # Cálculo das médias
    media_retorno = sum(tempos_retorno.values()) 
    media_resposta = sum(tempos_resposta.values()) 
    media_espera = sum(tempos_espera.values()) 
    tempoEsperaLista = [media_espera]
    tempoRespostaLista = [media_resposta]
    tempoRetornoLista = [media_retorno]
    imprimir_tabela_final(tempoChegadas, tempoEsperaLista, tempoRespostaLista, tempoRetornoLista, 2)

    
def imprimir_tabela_final(tempoChegadas, tempoEsperaLista, tempoRespostaLista, tempoRetornoLista, id):
    quantidadeProcessos = len(tempoChegadas)
    
    for i in range(quantidadeProcessos):
        tempoMedioEspera = sum(tempoEsperaLista) / quantidadeProcessos
        tempoMedioRetorno = sum(tempoRetornoLista) / quantidadeProcessos
        tempoMedioResposta = sum(tempoRespostaLista) / quantidadeProcessos

    
    if (id == 0):
         print("FCFS: {} {} {}".format(
        "{:.1f}".format(tempoMedioRetorno).replace('.', ','),
        "{:.1f}".format(tempoMedioResposta).replace('.', ','),
        "{:.1f}".format(tempoMedioEspera).replace('.', ',')
    ))
    elif(id == 1):
        print("SJF: {} {} {}".format(
        "{:.1f}".format(tempoMedioRetorno).replace('.', ','),
        "{:.1f}".format(tempoMedioResposta).replace('.', ','),
        "{:.1f}".format(tempoMedioEspera).replace('.', ',')
    ))
    elif(id == 2):
        print("RR: {} {} {}".format(
        "{:.1f}".format(tempoMedioRetorno).replace('.', ','),
        "{:.1f}".format(tempoMedioResposta).replace('.', ','),
        "{:.1f}".format(tempoMedioEspera).replace('.', ',')
    ))


arquivo = "testes.txt"
tempoChegadas, tempoPicos = ler_arquivo(arquivo)
FCFS(tempoChegadas, tempoPicos)
SJF(tempoChegadas,tempoPicos)
RR(tempoChegadas, tempoPicos,2)


