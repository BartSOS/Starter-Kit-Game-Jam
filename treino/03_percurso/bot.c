/* =============================================================================
 * GAME JAM PET 2026 - TREINO 03: Percorrer pontos em ordem (C99)
 * =============================================================================
 * Envie este arquivo na guia Treino e complete o TODO: o resto já funciona.
 * Mesmas regras do c/bot.c.
 * ============================================================================= */

#include "arena.h"   /* tipos Estado, Acao, Tanque, Inimigo, Hazard, Item e Ponto */

/* -----------------------------------------------------------------------------
 * AJUDANTES (opcional: renomeie, altere ou apague)
 * -----------------------------------------------------------------------------
 * Em C o estado já chega tipado (arena.h), então não há acessores: use direto
 *
 *   e->tick                           número do tick atual
 *   e->self                           seu tanque (Tanque)
 *   e->inimigos[i], i < e->n_inimigos adversários vivos (Inimigo)
 *   e->hazards[i],  i < e->n_hazards  perigos da arena (Hazard)
 *   e->itens[i],    i < e->n_itens    itens no mapa (Item)
 *
 * e devolva uma Acao com os campos throttle, turn, turret_angle, shoot e
 * shield (veja o pensar() abaixo). As funções abaixo são só matemática básica
 * (ângulos em graus; 0 = +x, cresce de +x para +y). Elas não decidem nada por
 * você.
 * ----------------------------------------------------------------------------- */

/* Distância entre dois pontos */
static inline double distancia(double x1, double y1, double x2, double y2) {
    return hypot(x2 - x1, y2 - y1);
}

/* Leva qualquer ângulo para o intervalo [0, 360) */
static inline double normalizar_angulo(double graus) {
    double a = fmod(graus, 360.0);
    return a < 0 ? a + 360.0 : a;
}

/* Ângulo, em graus, do ponto (x1, y1) olhando para o ponto (x2, y2) */
static inline double angulo_para(double x1, double y1, double x2, double y2) {
    return normalizar_angulo(atan2(y2 - y1, x2 - x1) * 180.0 / M_PI);
}

/* Menor giro, em graus, para ir do ângulo 'de' ao ângulo 'para': de -180 (exclusivo) a 180.
 * Positivo = girar no sentido em que o ângulo aumenta. */
static inline double diferenca_angulo(double de, double para) {
    double d = normalizar_angulo(para - de);
    return d > 180.0 ? d - 360.0 : d;
}

/* -----------------------------------------------------------------------------
 * FIM DOS AJUDANTES
 * ----------------------------------------------------------------------------- */


/* =============================================================================
 * SEU CÓDIGO COMEÇA AQUI
 * ============================================================================= */

static int proximo = 0;   /* índice do próximo ponto (static: vale entre os ticks) */

Acao pensar(const Estado *e) {
    const Tanque *meu = &e->self;
    Acao a = {0};
    a.turret_angle = meu->turret_angle;         /* em C a torre é sempre enviada */
    if (proximo >= e->n_pontos) return a;       /* terminou (ou fora do treino) */

    const Ponto *p = &e->pontos[proximo];       /* P1, P2... na ordem */
    double d = distancia(meu->x, meu->y, p->x, p->y);

    /* TODO: chegou (d <= p->raio)? Passe para o próximo ponto. */

    double giro = diferenca_angulo(meu->angle, angulo_para(meu->x, meu->y, p->x, p->y));
    a.throttle = 1.0;
    a.turn = fmax(-1.0, fmin(1.0, giro / 30.0));
    return a;
}
