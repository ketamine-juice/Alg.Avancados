"""
Módulo de funções auxiliares da função de Gibbs Sampling.
Código escrito por Rui Sousa com apoio a nível meta de LLM (GPT 3.5) para afinações de pseudo-código em certos casos.
Documentação gerada por Rui Sousa
"""

from random import choice, randint 

def escolhe_seq(seqs):
    '''
    Seleciona aleatoriamente uma sequência do conjunto de sequências.
    
    Retorna:
    - Tuple: (indice, escolhida), onde:
        * indice: índice da sequência selecionada
        * escolhida: sequência selecionada
    '''
    return choice(list(enumerate(seqs)))
   
def gerar_snips(seqs, tam_motif, offset_max, indice, escolhida):
    '''
    Gera snips para todas as sequências, exceto uma sequência escolhida aleatoriamente.
    
    Retorna:
    - Tuple: (offsets, snips), onde:
        * offsets: lista de offsets para cada sequência
        * snips: lista de snips para cada sequência
    '''
    offsets = [randint(0, offset_max) for pos, seq in enumerate(seqs) if pos != indice]
    snips = [seq[pos : pos + tam_motif] for seq, pos in zip(seqs, offsets) if seq != escolhida]

    return offsets, snips

def pwm(snips):
    '''
    Esta função difere da utilizada nas auxiliares, utilizando uma abordagem de lista de dicionários.
    
    Calcula a matriz de PWM (Position Weight Matrix) para uma lista de snips.
    
    Retorna:
    - List[dict]: lista de dicionários representando a matriz PWM
    '''
    return [{base: (seq.count(base) + 1) / (len(seq) + 4) for base in 'ACGT'} for seq in zip(*snips)]

def prob_snip(snip, P):
    '''
    Função que calcula a P(snip|P), para determinar a probabilidade
    deste ser gerado pelo perfil P

    Parâmetros:

    snip : str
        strings correspondente a bases de DNA

    P : list[dict]
        perfil probabilistico para um conjunto de sub-sequências de DNA

    Retorna:

    float
        P(snip|P)
    '''
    score = 1
    for pos, base in enumerate(snip):
        score *= P[pos][base]
    return score

def best_pos(snips, offsets, P):
    '''
    Encontra a melhor posição e offset.

    Retorna:
    - Tuple: (melhor_prob, melhor_offset), onde:
        * melhor_prob: melhor probabilidade
        * melhor_offset: melhor offset
    '''
    probs = [prob_snip(snip, P) for snip in snips]
    prob_sum = sum(probs)
    prob_comb = [round(prob / prob_sum, 5) for prob in probs]
    return max(zip(prob_comb, offsets))
