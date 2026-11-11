# =============================================================================
# GAME JAM PET 2026 - TREINO 06: Sobreviver à artilharia (Python 3)
# =============================================================================
# Complete os passos marcados com TODO dentro de pensar(). Do jeito que está,
# o modelo já roda, mas o tanque fica parado (e é destruído).
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
#   estado.perigos     lista dos bombardeios anunciados (Perigo: x, y, raio,
#                      frames_ate_impacto). Cada um aparece 30 frames antes
#                      de explodir.
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
#   Quem estiver a até uns 100 unidades do centro da explosão perde 40 de
#   vida. O tanque anda 5 unidades por frame.
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

    # PRONTO: achar o bombardeio que explode primeiro (o de menor
    # frames_ate_impacto). Às vezes há dois ao mesmo tempo.
    perigo = None                           # o mais urgente até agora; None = nenhum
    for p in estado.perigos:
        if perigo is None or p.frames_ate_impacto < perigo.frames_ate_impacto:
            perigo = p
    if perigo is None:
        return acao                         # nenhum perigo agora: fica parado

    if perigo.frames_ate_impacto == 10:     # depuração: uma linha por bombardeio
        print("frame", estado.frame, ": bombardeio em x =", round(perigo.x),
              "y =", round(perigo.y), "daqui a 10 frames")

    # TODO PASSO 1: calcule a distância do tanque até o centro do perigo,
    #   com distancia(meu.x, meu.y, perigo.x, perigo.y).

    # TODO PASSO 2: se a distância for maior que perigo.raio + 40, você já
    #   está seguro: return acao (fica parado).

    # TODO PASSO 3: fuja em linha reta, para longe do centro: a direção de
    #   fuga é o ângulo DO perigo PARA o tanque,
    #   fuga = angulo_para(perigo.x, perigo.y, meu.x, meu.y)
    #   (se a distância for menor que 1, o tanque está no centro e qualquer
    #   direção serve: use fuga = meu.angulo_chassi).
    #   Depois: acao.direcao = fuga e acao.mover = FRENTE

    # TODO PASSO 4: girar o chassi leva tempo (9 graus por frame). Se a fuga
    #   estiver atrás do tanque, é mais rápido andar de ré:
    #   se diferenca_angulo(meu.angulo_chassi, fuga) for maior que 90 ou
    #   menor que -90, use acao.mover = RE e acao.direcao = fuga + 180
    #   (de ré, a frente do chassi aponta para o lado oposto da fuga).

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
