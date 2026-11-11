# =============================================================================
# GAME JAM PET 2026 - STARTER KIT PYTHON 3
# =============================================================================
# Você escreve a função pensar(estado), logo abaixo. A arena chama pensar() uma
# vez por frame (1 frame = 0,1 segundo; 10 frames por segundo). Ela recebe o
# que o seu tanque enxerga (estado) e devolve o que ele faz neste frame (acao).
#
# REGRAS
# 1. Não leia a entrada (nada de input() nem sys.stdin): a arena já faz isso e
#    chama pensar() por você.
# 2. Escreva só dentro de pensar() e, se quiser, nas funções do fim do arquivo.
#    Não mude a linha "def pensar(estado):".
# 3. pensar() termina com "return acao": o que estiver em acao é o que o
#    tanque faz.
# 4. Para depurar, use print(...) e teste no seu computador com o verificar.py.
#    O print não chega à arena (o resultado do treino não o mostra).
# 5. Use só a biblioteca padrão do Python (math, random...). Bibliotecas de
#    fora (numpy etc.) e os módulos os, subprocess e importlib dão
#    Compilation Error.
# 6. Uma variável global (criada fora de pensar) guarda o valor de um frame
#    para o outro: é a memória do seu tanque. Para mudá-la dentro de pensar(),
#    escreva antes "global nome_da_variavel".
# 7. Você envia só este arquivo. O arena.py fica na mesma pasta e já está no
#    servidor.
#
# O QUE VOCÊ RECEBE (tudo explicado no arena.py)
#   estado.frame       número do frame (começa em 0)
#   estado.eu          o seu tanque (Tanque): x, y, angulo_chassi, angulo_torre,
#                      vida, energia, frames_para_atirar, escudo_ativo
#   estado.inimigos    lista dos inimigos vivos (Inimigo: id, x, y, vel_x, vel_y)
#   estado.perigos     lista dos perigos (Perigo: tipo, x, y, raio,
#                      frames_ate_impacto)
#   estado.itens       lista dos itens no mapa (Item: tipo, x, y)
#   estado.pontos      lista dos pontos das fases de treino (Ponto: id, x, y,
#                      raio); no torneio, vazia
#
# O QUE VOCÊ DEVOLVE (acao)
#   acao.mover          FRENTE, PARADO ou RE (0.5 = metade da velocidade)
#   acao.direcao        para onde o chassi deve apontar, em graus; ele gira
#                       até 9 graus por frame até chegar lá
#   acao.angulo_torre   para onde a torre aponta, em graus (chega na hora)
#   acao.atirar         True atira, False não atira
#   acao.ligar_escudo   True liga o escudo neste frame, False desliga
#   Ângulos: graus de 0 a 360; 0 aponta para +x e 90 aponta para +y.
# =============================================================================

from arena import *
import math


# =============================================================================
# SEU CÓDIGO COMEÇA AQUI
# =============================================================================

def pensar(estado):
    meu = estado.eu                         # o seu tanque: meu.x, meu.energia etc.

    # A ação começa parada: preencha sempre os 5 campos
    acao = Acao()
    acao.mover = PARADO
    acao.direcao = meu.angulo_chassi        # mantém a direção do chassi
    acao.angulo_torre = meu.angulo_torre    # mantém a torre
    acao.atirar = False
    acao.ligar_escudo = False

    # Para depurar (aparece no verificar.py):
    # print("frame", estado.frame, ": vida", meu.vida)

    # ---- EXEMPLO DE ESTRATÉGIA: troque pela sua ----

    # Passo 1: achar o inimigo mais perto
    alvo = None                             # o mais perto até agora; None = nenhum
    menor_distancia = 0
    for inimigo in estado.inimigos:
        d = distancia(meu.x, meu.y, inimigo.x, inimigo.y)
        if alvo is None or d < menor_distancia:
            alvo = inimigo
            menor_distancia = d
    if alvo is None:
        return acao                         # ninguém à vista: fica parado

    # Passo 2: apontar a torre para ele
    angulo_alvo = angulo_para(meu.x, meu.y, alvo.x, alvo.y)
    acao.angulo_torre = angulo_alvo

    # Passo 3: atirar quando puder (cada tiro gasta 20 de energia)
    if meu.frames_para_atirar == 0 and meu.energia >= 20:
        acao.atirar = True

    # Passo 4: andar. Longe, vai na direção dele; perto, anda de lado
    # (90 graus a mais) para ser um alvo difícil
    if menor_distancia > 300:
        acao.direcao = angulo_alvo
    else:
        acao.direcao = angulo_alvo + 90
    acao.mover = FRENTE

    return acao


# -----------------------------------------------------------------------------
# AJUDANTES (opcional: use, mude ou apague)
# -----------------------------------------------------------------------------
# Matemática básica, com ângulos em graus (0 aponta para +x; 90, para +y).
# Elas só calculam: não decidem nada por você.
# -----------------------------------------------------------------------------

# Distância entre o ponto (x1, y1) e o ponto (x2, y2)
def distancia(x1, y1, x2, y2):
    dx = x2 - x1                            # quanto falta em x
    dy = y2 - y1                            # quanto falta em y
    return math.sqrt(dx * dx + dy * dy)     # Pitágoras


# Ângulo, em graus (de 0 a 360), de quem está em (x1, y1) olhando para (x2, y2)
def angulo_para(x1, y1, x2, y2):
    radianos = math.atan2(y2 - y1, x2 - x1)     # atan2 devolve radianos, de -pi a pi
    graus = radianos * 180.0 / math.pi          # em graus: de -180 a 180
    if graus < 0:
        graus = graus + 360.0                   # passa para 0 a 360
    return graus


# Quanto girar para ir do ângulo "de" ao ângulo "para" pelo caminho mais
# curto: de -180 a 180 graus. Positivo = o ângulo aumenta; negativo = diminui.
def diferenca_angulo(de, para):
    d = para - de
    while d > 180.0:
        d = d - 360.0                       # mais de meia volta: vai pelo outro lado
    while d <= -180.0:
        d = d + 360.0
    return d

# -----------------------------------------------------------------------------
# FIM DOS AJUDANTES
# -----------------------------------------------------------------------------
