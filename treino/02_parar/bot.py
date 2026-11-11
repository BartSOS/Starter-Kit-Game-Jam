# =============================================================================
# GAME JAM PET 2026 - TREINO 02: Parar dentro do ponto B (Python 3)
# =============================================================================
# Complete os passos marcados com TODO dentro de pensar(). Do jeito que está,
# o modelo já roda, mas o tanque fica parado.
#
# REGRAS
# 1. Não leia a entrada (nada de input() nem sys.stdin): a arena já faz isso e
#    chama pensar() por você, uma vez por frame (1 frame = 0,1 segundo).
# 2. Escreva só dentro de pensar() e, se quiser, nas funções do fim do arquivo.
#    Não mude a linha "def pensar(estado):".
# 3. pensar() termina com "return acao": o que estiver em acao é o que o
#    tanque faz.
# 4. Para depurar, use print(...) e teste no seu computador com o verificar.py
#    (o resultado do treino não mostra o print).
# 5. Envie só este arquivo, na própria fase da guia Treino. O arena.py fica na
#    mesma pasta e já está no servidor.
#
# O QUE VOCÊ RECEBE (tudo explicado no arena.py)
#   estado.frame       número do frame (começa em 0)
#   estado.eu          o seu tanque (Tanque): x, y, angulo_chassi, angulo_torre,
#                      vida, energia, frames_para_atirar, escudo_ativo
#   estado.pontos      lista dos pontos da fase (Ponto: id, x, y, raio)
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
    meu = estado.eu                         # o seu tanque: meu.x, meu.angulo_chassi etc.

    # A ação começa parada: preencha sempre os 5 campos
    acao = Acao()
    acao.mover = PARADO
    acao.direcao = meu.angulo_chassi        # mantém a direção do chassi
    acao.angulo_torre = meu.angulo_torre    # mantém a torre
    acao.atirar = False
    acao.ligar_escudo = False

    # PRONTO: achar o ponto B, como na fase 01
    b = None                                # o ponto B; None = não achou
    for p in estado.pontos:
        if p.id == "B":
            b = p
    if b is None:
        return acao                         # fora do treino não há ponto B: fica parado
    # b.x, b.y: o centro; b.raio: o tamanho

    if estado.frame == 0:                   # depuração: mostra B só no primeiro frame
        print("ponto B em x =", round(b.x), "y =", round(b.y), "raio =", round(b.raio))

    # TODO PASSO 1: como na fase 01, calcule o ângulo até B com
    #   angulo_para(meu.x, meu.y, b.x, b.y) e ponha em acao.direcao.

    # TODO PASSO 2: calcule a distância do tanque até B, com
    #   distancia(meu.x, meu.y, b.x, b.y), e guarde numa variável.

    # TODO PASSO 3: se a distância for menor que b.raio, o tanque chegou:
    #   acao.mover = PARADO. Se não, acao.mover = FRENTE.
    #   Não há inércia: com PARADO o tanque para no mesmo frame.

    # PASSO 4 (opcional, se o tanque passar do ponto): ele anda 5 unidades
    #   por frame. Se faltar menos que isso, ande só o que falta:
    #   acao.mover = distância / 5 (0.5 anda 2,5 unidades).

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
