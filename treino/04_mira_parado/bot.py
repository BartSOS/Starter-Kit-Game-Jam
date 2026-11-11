# =============================================================================
# GAME JAM PET 2026 - TREINO 04: Acertar alvos parados (Python 3)
# =============================================================================
# Complete os passos marcados com TODO dentro de pensar(). Do jeito que está,
# o modelo já roda, mas o tanque não atira.
#
# REGRAS
# 1. Não leia a entrada (nada de input() nem sys.stdin): a arena já faz isso e
#    chama pensar() por você, uma vez por frame (1 frame = 0,1 segundo).
# 2. Escreva só dentro de pensar() e, se quiser, nas funções do fim do arquivo
#    e nas variáveis globais. Não mude a linha "def pensar(estado):".
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
#   estado.inimigos    lista dos alvos vivos (Inimigo: id, x, y, vel_x, vel_y).
#                      Um alvo destruído sai da lista.
#
# O QUE VOCÊ DEVOLVE (acao)
#   acao.mover          FRENTE, PARADO ou RE (0.5 = metade da velocidade)
#   acao.direcao        para onde o chassi deve apontar, em graus; ele gira
#                       até 9 graus por frame até chegar lá
#   acao.angulo_torre   para onde a torre aponta, em graus (chega na hora)
#   acao.atirar         True atira, False não atira
#   acao.ligar_escudo   True liga o escudo neste frame, False desliga
#   Ângulos: graus de 0 a 360; 0 aponta para +x e 90 aponta para +y.
#
#   O tiro só sai se acao.atirar = True, meu.frames_para_atirar for 0 e
#   meu.energia for pelo menos 20 (cada tiro gasta 20).
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

    if len(estado.inimigos) == 0:
        return acao                         # nenhum alvo vivo: nada a fazer

    # PRONTO: escolher o alvo. Aqui é sempre o primeiro da lista.
    alvo = estado.inimigos[0]

    if estado.frame == 0:                   # depuração: mostra o primeiro alvo
        print("alvo", alvo.id, "em x =", round(alvo.x), "y =", round(alvo.y))

    # TODO PASSO 1: aponte a torre para o alvo: ponha em acao.angulo_torre
    #   o ângulo angulo_para(meu.x, meu.y, alvo.x, alvo.y).

    # TODO PASSO 2: atire (acao.atirar = True) só se o tiro puder sair:
    #   meu.frames_para_atirar igual a 0 e meu.energia de pelo menos 20.

    # TODO PASSO 3 (para 3 balões): enquanto o tiro voa, o alvo continua
    #   na lista, e o passo 2 atira nele de novo. Para não gastar tiro:
    #   a) crie, fora de pensar, uma lista global com os ids que já levaram
    #      tiro: atirados = []
    #   b) ao atirar, guarde o id: atirados.append(alvo.id) (o append muda
    #      a lista sem precisar de "global");
    #   c) no lugar do "PRONTO" acima, escolha com um laço o primeiro
    #      inimigo cujo id não está em atirados (inimigo.id not in atirados).

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
