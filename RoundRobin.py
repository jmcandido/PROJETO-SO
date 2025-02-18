from collections import deque

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


def RR(tempos_chegada, tempos_execucao, quantum):
   
    processos = [(i + 1, tempos_chegada[i], tempos_execucao[i]) for i in range(len(tempos_chegada))]
    processos.sort(key=lambda x: x[1])  # Ordenação pelo tempo de chegada
    
    fila = deque()
    tempo_atual = 0
    indice_processo = 0
    tempos_retorno = {}  # Tempo de retorno de cada processo
    tempos_resposta = {}  # Tempo de resposta de cada processo
    execucoes = {}  # Momento da primeira execução de cada processo
    tempos_espera = {p[0]: 0 for p in processos}  # Tempo de espera de cada processo

    while fila or indice_processo < len(processos):
        while indice_processo < len(processos) and processos[indice_processo][1] <= tempo_atual:
            fila.append([processos[indice_processo][0], processos[indice_processo][2], processos[indice_processo][1]])  # (ID, Tempo Restante, Tempo Chegada)
            indice_processo += 1
        
        if fila:
            id_processo, tempo_restante, tempo_chegada = fila.popleft()
            
            if id_processo not in execucoes:
                tempos_resposta[id_processo] = tempo_atual - tempo_chegada  # Tempo da primeira execução
                execucoes[id_processo] = tempo_atual
            
            tempo_execucao = min(quantum, tempo_restante)
            tempo_atual += tempo_execucao

            while indice_processo < len(processos) and processos[indice_processo][1] <= tempo_atual:
                fila.append([processos[indice_processo][0], processos[indice_processo][2], processos[indice_processo][1]])
                indice_processo += 1
            
            if tempo_restante > quantum:
                fila.append([id_processo, tempo_restante - quantum, tempo_chegada])
            else:
                tempos_retorno[id_processo] = tempo_atual - tempo_chegada  # Tempo de retorno

        else:
            tempo_atual += 1

    # Cálculo dos tempos de espera
    for id_processo in tempos_retorno:
        tempo_pico = [p[2] for p in processos if p[0] == id_processo][0]  # O tempo de pico é o tempo de execução
        tempos_espera[id_processo] = tempos_retorno[id_processo] - tempo_pico

    # Cálculo das médias
    media_retorno = sum(tempos_retorno.values()) / len(tempos_retorno)
    media_resposta = sum(tempos_resposta.values()) / len(tempos_resposta)
    media_espera = sum(tempos_espera.values()) / len(tempos_espera)
    
    return f"RR {media_retorno:.1f} {media_resposta:.1f} {media_espera:.1f}"

# Leitura do arquivo mantendo sua função original
nome_arquivo = "testes.txt"
tempos_chegada, tempos_picos = ler_arquivo(nome_arquivo)

# Definir quantum
quantum = 2  

# Executar o escalonador Round Robin e exibir o resultado
resultado = RR(tempos_chegada, tempos_picos, quantum)
print(resultado)
