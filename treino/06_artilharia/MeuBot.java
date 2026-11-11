// =============================================================================
// GAME JAM PET 2026 - TREINO 06: Sobreviver à artilharia (Java)
// =============================================================================
// Complete os passos marcados com TODO dentro de pensar(). Do jeito que está,
// o modelo já compila e roda, mas o tanque fica parado (e é destruído).
//
// REGRAS
// 1. Não escreva main() nem leia o teclado (Scanner, System.in): a arena já
//    tem o main dela e chama pensar() por você, uma vez por frame
//    (1 frame = 0,1 segundo).
// 2. Escreva só dentro de pensar() e, se quiser, nos métodos do fim da classe
//    e nas variáveis static. Não mude as linhas "public class MeuBot extends
//    Arena" e "public static Acao pensar(Estado e)". Não use "package".
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
//   e.perigos[i]      bombardeios anunciados (Perigo: x, y, raio,
//                     frames_ate_impacto); são e.n_perigos. Cada um aparece
//                     30 frames antes de explodir.
//
// O QUE VOCÊ DEVOLVE (acao)
//   acao.mover          FRENTE, PARADO ou RE (0.5 = metade da velocidade)
//   acao.direcao        para onde o chassi deve apontar, em graus; ele gira
//                       até 9 graus por frame até chegar lá
//   acao.angulo_torre   para onde a torre aponta, em graus (chega na hora)
//   acao.atirar         true atira, false não atira
//   acao.ligar_escudo   true liga o escudo neste frame, false desliga
//   Ângulos: graus de 0 a 360; 0 aponta para +x e 90 aponta para +y.
//
//   Quem estiver a até uns 100 unidades do centro da explosão perde 40 de
//   vida. O tanque anda 5 unidades por frame.
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

        // PRONTO: achar o bombardeio que explode primeiro (o de menor
        // frames_ate_impacto). Às vezes há dois ao mesmo tempo.
        int mais_urgente = -1;                  // índice em perigos; -1 = nenhum
        for (int i = 0; i < e.n_perigos; i++) {
            Perigo p = e.perigos[i];
            if (mais_urgente == -1 || p.frames_ate_impacto < e.perigos[mais_urgente].frames_ate_impacto) {
                mais_urgente = i;
            }
        }
        if (mais_urgente == -1) {
            return acao;                        // nenhum perigo agora: fica parado
        }
        Perigo perigo = e.perigos[mais_urgente];

        if (perigo.frames_ate_impacto == 10) {  // depuração: uma linha por bombardeio
            System.err.println("frame " + e.frame + ": bombardeio em (" + perigo.x + ", "
                    + perigo.y + ") daqui a 10 frames");
        }

        // TODO PASSO 1: calcule a distância do tanque até o centro do perigo,
        //   com distancia(meu.x, meu.y, perigo.x, perigo.y).

        // TODO PASSO 2: se a distância for maior que perigo.raio + 40, você já
        //   está seguro: return acao; (fica parado).

        // TODO PASSO 3: fuja em linha reta, para longe do centro: a direção de
        //   fuga é o ângulo DO perigo PARA o tanque,
        //   double fuga = angulo_para(perigo.x, perigo.y, meu.x, meu.y);
        //   (se a distância for menor que 1, o tanque está no centro e qualquer
        //   direção serve: use fuga = meu.angulo_chassi).
        //   Depois: acao.direcao = fuga; acao.mover = FRENTE;

        // TODO PASSO 4: girar o chassi leva tempo (9 graus por frame). Se a fuga
        //   estiver atrás do tanque, é mais rápido andar de ré:
        //   se diferenca_angulo(meu.angulo_chassi, fuga) for maior que 90 ou
        //   menor que -90, use acao.mover = RE e acao.direcao = fuga + 180
        //   (de ré, a frente do chassi aponta para o lado oposto da fuga).

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
