// =============================================================================
// GAME JAM PET 2026 - TREINO 02: Parar dentro do ponto B (Java)
// =============================================================================
// Complete os passos marcados com TODO dentro de pensar(). Do jeito que está,
// o modelo já compila e roda, mas o tanque fica parado.
//
// REGRAS
// 1. Não escreva main() nem leia o teclado (Scanner, System.in): a arena já
//    tem o main dela e chama pensar() por você, uma vez por frame
//    (1 frame = 0,1 segundo).
// 2. Escreva só dentro de pensar() e, se quiser, nos métodos do fim da classe.
//    Não mude as linhas "public class MeuBot extends Arena" e
//    "public static Acao pensar(Estado e)". Não use "package".
// 3. pensar() termina com "return acao;": o que estiver em acao é o que o
//    tanque faz.
// 4. Não use System.out: a arena usa a saída do programa. Para depurar, use
//    System.err.println(...) e teste no seu computador com o verificar.py
//    (o resultado do treino não mostra o System.err).
// 5. Envie só este arquivo, na própria fase da guia Treino. O Arena.java fica
//    na mesma pasta e já está no servidor.
//
// O QUE VOCÊ RECEBE (tudo explicado no Arena.java)
//   e.frame           número do frame (começa em 0)
//   e.eu              o seu tanque (Tanque): x, y, angulo_chassi, angulo_torre,
//                     vida, energia, frames_para_atirar, escudo_ativo
//   e.pontos[i]       pontos da fase (Ponto: id, x, y, raio); são e.n_pontos
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
        Tanque meu = e.eu;                      // o seu tanque: meu.x, meu.angulo_chassi etc.

        // A ação começa parada: preencha sempre os 5 campos
        Acao acao = new Acao();
        acao.mover = PARADO;
        acao.direcao = meu.angulo_chassi;       // mantém a direção do chassi
        acao.angulo_torre = meu.angulo_torre;   // mantém a torre
        acao.atirar = false;
        acao.ligar_escudo = false;

        // PRONTO: achar o ponto B, como na fase 01
        int indice_b = -1;                      // posição de B na lista; -1 = não achou
        for (int i = 0; i < e.n_pontos; i++) {
            Ponto p = e.pontos[i];
            if (p.id.equals("B")) {
                indice_b = i;
            }
        }
        if (indice_b == -1) {
            return acao;                        // fora do treino não há ponto B: fica parado
        }
        Ponto b = e.pontos[indice_b];           // b.x, b.y: o centro; b.raio: o tamanho

        if (e.frame == 0) {                     // depuração: mostra B só no primeiro frame
            System.err.println("ponto B em (" + b.x + ", " + b.y + "), raio " + b.raio);
        }

        // TODO PASSO 1: como na fase 01, calcule o ângulo até B com
        //   angulo_para(meu.x, meu.y, b.x, b.y) e ponha em acao.direcao.

        // TODO PASSO 2: calcule a distância do tanque até B, com
        //   distancia(meu.x, meu.y, b.x, b.y), e guarde numa variável double.

        // TODO PASSO 3: se a distância for menor que b.raio, o tanque chegou:
        //   acao.mover = PARADO. Se não, acao.mover = FRENTE.
        //   Não há inércia: com PARADO o tanque para no mesmo frame.

        // PASSO 4 (opcional, se o tanque passar do ponto): ele anda 5 unidades
        //   por frame. Se faltar menos que isso, ande só o que falta:
        //   acao.mover = distância / 5 (0.5 anda 2,5 unidades).

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
