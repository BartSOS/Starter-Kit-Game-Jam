// =============================================================================
// GAME JAM PET 2026 - TREINO 03: Percorrer os pontos em ordem (C++20)
// =============================================================================
// Complete os passos marcados com TODO dentro de pensar(). Do jeito que está,
// o modelo já compila e roda, mas o tanque fica parado.
//
// REGRAS
// 1. Não escreva main(): a arena já tem a dela e chama pensar() por você,
//    uma vez por frame (1 frame = 0,1 segundo).
// 2. Escreva só dentro de pensar() e, se quiser, nas funções do fim do arquivo
//    e nas variáveis globais. Não mude a linha "Acao pensar(const Estado& e)".
// 3. pensar() termina com "return acao;": o que estiver em acao é o que o
//    tanque faz.
// 4. Não use cout nem cin: a arena usa a entrada e a saída do programa.
//    Para depurar, use cerr << ... e teste no seu computador com o
//    verificar.py (o resultado do treino não mostra o cerr).
// 5. Uma variável global (fora de pensar) guarda o valor de um frame para o
//    outro: é a memória do tanque.
// 6. Envie só este arquivo, na própria fase da guia Treino. O arena.hpp fica na
//    mesma pasta e já está no servidor.
//
// O QUE VOCÊ RECEBE (tudo explicado no arena.hpp)
//   e.frame           número do frame (começa em 0)
//   e.eu              o seu tanque (Tanque): x, y, angulo_chassi, angulo_torre,
//                     vida, energia, frames_para_atirar, escudo_ativo
//   e.pontos[i]      pontos da fase (Ponto: id, x, y, raio); são e.n_pontos
//
// O QUE VOCÊ DEVOLVE (acao)
//   acao.mover          FRENTE, PARADO ou RE (0.5 = metade da velocidade)
//   acao.direcao        para onde o chassi deve apontar, em graus; ele gira
//                       até 9 graus por frame até chegar lá
//   acao.angulo_torre   para onde a torre aponta, em graus (chega na hora)
//   acao.atirar         true atira, false não atira
//   acao.ligar_escudo   true liga o escudo neste frame, false desliga
//   Ângulos: graus de 0 a 360; 0 aponta para +x e 90 aponta para +y.
// =============================================================================

#include "arena.hpp"
using namespace std;

// Estas funções estão no fim do arquivo (AJUDANTES)
double distancia(double x1, double y1, double x2, double y2);
double angulo_para(double x1, double y1, double x2, double y2);
double diferenca_angulo(double de, double para);


// =============================================================================
// SEU CÓDIGO COMEÇA AQUI
// =============================================================================

// Memória do tanque: o estado não diz por quais pontos você já passou
string ordem[4] = {"P1", "P2", "P3", "P4"};   // os pontos, na ordem pedida
int proximo = 0;                              // índice em ordem[] do próximo ponto

Acao pensar(const Estado& e) {
    Tanque meu = e.eu;                      // o seu tanque: meu.x, meu.energia etc.

    // A ação começa parada: preencha sempre os 5 campos
    Acao acao;
    acao.mover = PARADO;
    acao.direcao = meu.angulo_chassi;       // mantém a direção do chassi
    acao.angulo_torre = meu.angulo_torre;   // mantém a torre
    acao.atirar = false;
    acao.ligar_escudo = false;

    if (proximo == 4) {
        return acao;                        // passou pelos 4: pode parar
    }

    // PRONTO: achar na lista o ponto cujo id é ordem[proximo] ("P1", depois
    // "P2"...). O ponto mais perto quase nunca é o próximo.
    int indice = -1;                        // -1 = não achou
    for (int i = 0; i < e.n_pontos; i++) {
        Ponto p = e.pontos[i];
        if (p.id == ordem[proximo]) {
            indice = i;
        }
    }
    if (indice == -1) {
        return acao;                        // fora do treino não há pontos: fica parado
    }
    Ponto alvo = e.pontos[indice];

    if (e.frame == 0) {                     // depuração: mostra o primeiro ponto
        cerr << alvo.id << " em (" << alvo.x << ", " << alvo.y << ")" << endl;
    }

    // TODO PASSO 1: calcule a distância do tanque até o alvo, com
    //   distancia(meu.x, meu.y, alvo.x, alvo.y).

    // TODO PASSO 2: se a distância for menor que alvo.raio, você chegou a
    //   esse ponto: some 1 em proximo (proximo = proximo + 1) e devolva a
    //   ação (return acao;). No frame seguinte o laço já procura o próximo.

    // TODO PASSO 3: ponha em acao.direcao o ângulo até o alvo, com
    //   angulo_para(meu.x, meu.y, alvo.x, alvo.y).

    // TODO PASSO 4: ande para a frente: acao.mover = FRENTE.

    return acao;
}


// -----------------------------------------------------------------------------
// AJUDANTES (opcional: use, mude ou apague)
// -----------------------------------------------------------------------------
// Matemática básica, com ângulos em graus (0 aponta para +x; 90, para +y).
// Elas só calculam: não decidem nada por você.
// -----------------------------------------------------------------------------

// Distância entre o ponto (x1, y1) e o ponto (x2, y2)
double distancia(double x1, double y1, double x2, double y2) {
    double dx = x2 - x1;                    // quanto falta em x
    double dy = y2 - y1;                    // quanto falta em y
    return sqrt(dx * dx + dy * dy);         // Pitágoras
}

// Ângulo, em graus (de 0 a 360), de quem está em (x1, y1) olhando para (x2, y2)
double angulo_para(double x1, double y1, double x2, double y2) {
    double radianos = atan2(y2 - y1, x2 - x1);  // atan2 devolve radianos, de -pi a pi
    double graus = radianos * 180.0 / M_PI;     // em graus: de -180 a 180
    if (graus < 0) {
        graus = graus + 360.0;                  // passa para 0 a 360
    }
    return graus;
}

// Quanto girar para ir do ângulo "de" ao ângulo "para" pelo caminho mais
// curto: de -180 a 180 graus. Positivo = o ângulo aumenta; negativo = diminui.
double diferenca_angulo(double de, double para) {
    double d = para - de;
    while (d > 180.0) {
        d = d - 360.0;                      // mais de meia volta: vai pelo outro lado
    }
    while (d <= -180.0) {
        d = d + 360.0;
    }
    return d;
}

// -----------------------------------------------------------------------------
// FIM DOS AJUDANTES
// -----------------------------------------------------------------------------
