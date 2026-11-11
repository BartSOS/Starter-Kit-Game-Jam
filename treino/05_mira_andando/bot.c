/* =============================================================================
 * GAME JAM PET 2026 - TREINO 05: Acertar alvos andando (C99)
 * =============================================================================
 * Complete os passos marcados com TODO dentro de pensar(). Do jeito que está,
 * o modelo já compila e roda, mas o tanque fica parado.
 *
 * REGRAS
 * 1. Não escreva main(): a arena já tem a dela e chama pensar() por você,
 *    uma vez por frame (1 frame = 0,1 segundo).
 * 2. Escreva só dentro de pensar() e, se quiser, nas funções do fim do arquivo
 *    e nas variáveis globais. Não mude a linha "Acao pensar(const Estado *e)".
 * 3. pensar() termina com "return acao;": o que estiver em acao é o que o
 *    tanque faz.
 * 4. Não use printf nem scanf: a arena usa a entrada e a saída do programa.
 *    Para depurar, use fprintf(stderr, ...) e teste no seu computador com o
 *    verificar.py (o resultado do treino não mostra o stderr).
 * 5. Uma variável global (fora de pensar) guarda o valor de um frame para o
 *    outro: é a memória do tanque.
 * 6. Envie só este arquivo, na própria fase da guia Treino. O arena.h fica na
 *    mesma pasta e já está no servidor.
 *
 * O QUE VOCÊ RECEBE (tudo explicado no arena.h)
 *   e->frame          número do frame (começa em 0)
 *   e->eu             o seu tanque (Tanque): x, y, angulo_chassi, angulo_torre,
 *                     vida, energia, frames_para_atirar, escudo_ativo
 *   e->pontos[i]      pontos da fase (Ponto: id, x, y, raio); são e->n_pontos
 *   e->inimigos[i]    alvos vivos (Inimigo: id, x, y, vel_x, vel_y); são
 *                     e->n_inimigos. Um alvo destruído sai da lista.
 *   Por que "e->" e não "e.": e é um ponteiro (o endereço do estado). Copie o
 *   que precisar para uma variável comum, como em "Tanque meu = e->eu;" ou
 *   "Inimigo alvo = e->inimigos[i];", e use o ponto daí em diante: alvo.x.
 *
 * O QUE VOCÊ DEVOLVE (acao)
 *   acao.mover          FRENTE, PARADO ou RE (0.5 = metade da velocidade)
 *   acao.direcao        para onde o chassi deve apontar, em graus; ele gira
 *                       até 9 graus por frame até chegar lá
 *   acao.angulo_torre   para onde a torre aponta, em graus (chega na hora)
 *   acao.atirar         1 atira, 0 não atira
 *   acao.ligar_escudo   1 liga o escudo neste frame, 0 desliga
 *   Ângulos: graus de 0 a 360; 0 aponta para +x e 90 aponta para +y.
 *
 *   O chassi (mover, direcao) e a torre (angulo_torre, atirar) são
 *   independentes: no mesmo frame o tanque anda para um lado e atira para
 *   outro. O tiro só sai se acao.atirar = 1, meu.frames_para_atirar for 0 e
 *   meu.energia for pelo menos 20 (cada tiro gasta 20; ela volta 0,5 por
 *   frame).
 * ============================================================================= */

#include "arena.h"

/* Estas funções estão no fim do arquivo (AJUDANTES) */
double distancia(double x1, double y1, double x2, double y2);
double angulo_para(double x1, double y1, double x2, double y2);
double diferenca_angulo(double de, double para);


/* =============================================================================
 * SEU CÓDIGO COMEÇA AQUI
 * ============================================================================= */

Acao pensar(const Estado *e) {
    /* O seu tanque. Esta é a única seta (->) que você precisa: daqui em
     * diante use meu.x, meu.angulo_chassi etc. */
    Tanque meu = e->eu;

    /* A ação começa parada: preencha sempre os 5 campos */
    Acao acao;
    acao.mover = PARADO;
    acao.direcao = meu.angulo_chassi;       /* mantém a direção do chassi */
    acao.angulo_torre = meu.angulo_torre;   /* mantém a torre */
    acao.atirar = 0;
    acao.ligar_escudo = 0;

    /* PRONTO: achar o ponto B, como na fase 01 */
    int indice_b = -1;                      /* -1 = não achou */
    for (int i = 0; i < e->n_pontos; i++) {
        Ponto p = e->pontos[i];
        if (strcmp(p.id, "B") == 0) {
            indice_b = i;
        }
    }
    if (indice_b == -1) {
        return acao;                        /* fora do treino não há ponto B: fica parado */
    }
    Ponto b = e->pontos[indice_b];

    if (e->frame == 0) {                    /* depuração: mostra B e os alvos */
        fprintf(stderr, "ponto B em (%.0f, %.0f); %d alvos\n", b.x, b.y, e->n_inimigos);
    }

    /* TODO PASSO 1 (chassi): vá até B sem parar, como na fase 01:
     *   acao.direcao = angulo_para(meu.x, meu.y, b.x, b.y) e
     *   acao.mover = FRENTE. Não dá tempo de parar para atirar. */

    /* TODO PASSO 2 (torre): ache o alvo mais perto do tanque. Um jeito:
     *   int mais_perto = -1;              (índice do melhor até agora)
     *   double menor_distancia = 0;
     *   para cada i de 0 até e->n_inimigos - 1:
     *       Inimigo inimigo = e->inimigos[i];
     *       calcule d = distancia(meu.x, meu.y, inimigo.x, inimigo.y);
     *       se mais_perto == -1 ou d < menor_distancia:
     *           mais_perto = i; menor_distancia = d;
     *   Se mais_perto continuar -1, não há alvo: return acao;
     *   Se não, copie: Inimigo alvo = e->inimigos[mais_perto]; */

    /* TODO PASSO 3: aponte a torre para o alvo: acao.angulo_torre =
     *   angulo_para(meu.x, meu.y, alvo.x, alvo.y). Os alvos não se mexem,
     *   então mire da sua posição atual. */

    /* TODO PASSO 4: atire (acao.atirar = 1) só se meu.frames_para_atirar
     *   for 0 e meu.energia for pelo menos 20. */

    /* TODO PASSO 5 (para mais balões): a energia é justa, e um tiro repetido
     *   no mesmo alvo custa 40 frames de espera. Como na fase 04, guarde
     *   numa lista global os ids que já levaram tiro e, no passo 2, pule os
     *   inimigos cujo id está nela. */

    return acao;
}


/* -----------------------------------------------------------------------------
 * AJUDANTES (opcional: use, mude ou apague)
 * -----------------------------------------------------------------------------
 * Matemática básica, com ângulos em graus (0 aponta para +x; 90, para +y).
 * Elas só calculam: não decidem nada por você.
 * ----------------------------------------------------------------------------- */

/* Distância entre o ponto (x1, y1) e o ponto (x2, y2) */
double distancia(double x1, double y1, double x2, double y2) {
    double dx = x2 - x1;                    /* quanto falta em x */
    double dy = y2 - y1;                    /* quanto falta em y */
    return sqrt(dx * dx + dy * dy);         /* Pitágoras */
}

/* Ângulo, em graus (de 0 a 360), de quem está em (x1, y1) olhando para (x2, y2) */
double angulo_para(double x1, double y1, double x2, double y2) {
    double radianos = atan2(y2 - y1, x2 - x1);  /* atan2 devolve radianos, de -pi a pi */
    double graus = radianos * 180.0 / M_PI;     /* em graus: de -180 a 180 */
    if (graus < 0) {
        graus = graus + 360.0;                  /* passa para 0 a 360 */
    }
    return graus;
}

/* Quanto girar para ir do ângulo "de" ao ângulo "para" pelo caminho mais
 * curto: de -180 a 180 graus. Positivo = o ângulo aumenta; negativo = diminui. */
double diferenca_angulo(double de, double para) {
    double d = para - de;
    while (d > 180.0) {
        d = d - 360.0;                      /* mais de meia volta: vai pelo outro lado */
    }
    while (d <= -180.0) {
        d = d + 360.0;
    }
    return d;
}

/* -----------------------------------------------------------------------------
 * FIM DOS AJUDANTES
 * ----------------------------------------------------------------------------- */
