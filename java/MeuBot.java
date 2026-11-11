// =============================================================================
// GAME JAM PET 2026 - STARTER KIT JAVA
// =============================================================================
// Você escreve o método pensar(), logo abaixo. A arena chama pensar() uma vez
// por frame (1 frame = 0,1 segundo; 10 frames por segundo). Ele recebe o que o
// seu tanque enxerga (e) e devolve o que ele faz neste frame (acao).
//
// REGRAS
// 1. Não escreva main() nem leia o teclado (Scanner, System.in): a arena já
//    tem o main dela e chama pensar() por você.
// 2. Escreva só dentro de pensar() e, se quiser, nos métodos do fim da classe.
//    Não mude as linhas "public class MeuBot extends Arena" e
//    "public static Acao pensar(Estado e)". Não use "package".
// 3. pensar() termina com "return acao;": o que estiver em acao é o que o
//    tanque faz.
// 4. Não use System.out: a arena usa a saída do programa. Para depurar, use
//    System.err.println(...) e teste no seu computador com o verificar.py
//    (o resultado do treino não mostra o System.err).
// 5. Todo método e toda variável criada fora de pensar() levam "static".
//    Uma variável static guarda o valor de um frame para o outro: é a
//    memória do seu tanque.
// 6. Você envia só este arquivo. O Arena.java fica na mesma pasta e já está
//    no servidor.
//
// O QUE VOCÊ RECEBE (tudo explicado no Arena.java)
//   e.frame           número do frame (começa em 0)
//   e.eu              o seu tanque (Tanque): x, y, angulo_chassi, angulo_torre,
//                     vida, energia, frames_para_atirar, escudo_ativo
//   e.inimigos[i]     inimigos vivos (Inimigo: id, x, y, vel_x, vel_y);
//                     são e.n_inimigos
//   e.perigos[i]      perigos (Perigo: tipo, x, y, raio, frames_ate_impacto);
//                     são e.n_perigos
//   e.itens[i]        itens no mapa (Item: tipo, x, y); são e.n_itens
//   e.pontos[i]       pontos das fases de treino (Ponto: id, x, y, raio);
//                     são e.n_pontos (no torneio, 0)
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

public class MeuBot extends Arena {

    // =========================================================================
    // SEU CÓDIGO COMEÇA AQUI
    // =========================================================================

    public static Acao pensar(Estado e) {
        Tanque meu = e.eu;                      // o seu tanque: meu.x, meu.energia etc.

        // A ação começa parada: preencha sempre os 5 campos
        Acao acao = new Acao();
        acao.mover = PARADO;
        acao.direcao = meu.angulo_chassi;       // mantém a direção do chassi
        acao.angulo_torre = meu.angulo_torre;   // mantém a torre
        acao.atirar = false;
        acao.ligar_escudo = false;

        // Para depurar (aparece no verificar.py):
        // System.err.println("frame " + e.frame + ": vida " + meu.vida);

        // ---- EXEMPLO DE ESTRATÉGIA: troque pela sua ----

        // Passo 1: achar o inimigo mais perto
        int mais_perto = -1;                    // posição dele na lista; -1 = nenhum
        double menor_distancia = 0;
        for (int i = 0; i < e.n_inimigos; i++) {
            Inimigo inimigo = e.inimigos[i];
            double d = distancia(meu.x, meu.y, inimigo.x, inimigo.y);
            if (mais_perto == -1 || d < menor_distancia) {
                mais_perto = i;
                menor_distancia = d;
            }
        }
        if (mais_perto == -1) {
            return acao;                        // ninguém à vista: fica parado
        }
        Inimigo alvo = e.inimigos[mais_perto];

        // Passo 2: apontar a torre para ele
        double angulo_alvo = angulo_para(meu.x, meu.y, alvo.x, alvo.y);
        acao.angulo_torre = angulo_alvo;

        // Passo 3: atirar quando puder (cada tiro gasta 20 de energia)
        if (meu.frames_para_atirar == 0 && meu.energia >= 20) {
            acao.atirar = true;
        }

        // Passo 4: andar. Longe, vai na direção dele; perto, anda de lado
        // (90 graus a mais) para ser um alvo difícil
        if (menor_distancia > 300) {
            acao.direcao = angulo_alvo;
        } else {
            acao.direcao = angulo_alvo + 90;
        }
        acao.mover = FRENTE;

        return acao;
    }


    // -------------------------------------------------------------------------
    // AJUDANTES (opcional: use, mude ou apague)
    // -------------------------------------------------------------------------
    // Matemática básica, com ângulos em graus (0 aponta para +x; 90, para +y).
    // Elas só calculam: não decidem nada por você.
    // -------------------------------------------------------------------------

    // Distância entre o ponto (x1, y1) e o ponto (x2, y2)
    public static double distancia(double x1, double y1, double x2, double y2) {
        double dx = x2 - x1;                    // quanto falta em x
        double dy = y2 - y1;                    // quanto falta em y
        return Math.sqrt(dx * dx + dy * dy);    // Pitágoras
    }

    // Ângulo, em graus (de 0 a 360), de quem está em (x1, y1) olhando para (x2, y2)
    public static double angulo_para(double x1, double y1, double x2, double y2) {
        double radianos = Math.atan2(y2 - y1, x2 - x1);  // atan2 devolve radianos, de -pi a pi
        double graus = radianos * 180.0 / Math.PI;       // em graus: de -180 a 180
        if (graus < 0) {
            graus = graus + 360.0;                       // passa para 0 a 360
        }
        return graus;
    }

    // Quanto girar para ir do ângulo "de" ao ângulo "para" pelo caminho mais
    // curto: de -180 a 180 graus. Positivo = o ângulo aumenta; negativo = diminui.
    public static double diferenca_angulo(double de, double para) {
        double d = para - de;
        while (d > 180.0) {
            d = d - 360.0;                      // mais de meia volta: vai pelo outro lado
        }
        while (d <= -180.0) {
            d = d + 360.0;
        }
        return d;
    }

    // -------------------------------------------------------------------------
    // FIM DOS AJUDANTES
    // -------------------------------------------------------------------------
}
