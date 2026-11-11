# Ajudantes e arquivo de apoio do starter kit

Documento de manutenção (não vai no `starter_kit.zip`). Substitui o antigo contrato C-K1, de quando o
`pensar` recebia o JSON bruto da engine (`self`, `enemies`, `tick`...) e devolvia `throttle`/`turn`/`shoot`.

## Princípio

O desafio do participante é a lógica de decisão, não entender o sistema. Por isso:

- **tudo o que a equipe vê é em português**: os campos do estado, a ação, as constantes e as mensagens.
  A engine, o protocolo, o replay e a Unity continuam em inglês; o **arquivo de apoio** de cada
  linguagem traduz nos dois sentidos;
- a única unidade de tempo é o **frame** (1 frame = 0,1 s); velocidades em unidades por frame;
- o modelo traz `pensar()` no topo e os ajudantes no fim do arquivo, numa seção marcada
  `AJUDANTES (opcional: use, mude ou apague)` ... `FIM DOS AJUDANTES`. Os ajudantes só calculam:
  nenhum decide nada (nada de "inimigo mais próximo", fuga ou mira prontos);
- o código do modelo é de Programação 1: laços com índice ou `for x in lista`, `if`, funções
  simples. Em C e C++, sem `static`, `inline`, `fmod`, `hypot` e `? :`; os protótipos dos ajudantes
  ficam logo depois dos includes. Em C, o `->` aparece só em `Tanque meu = e->eu;`. Java exige
  `static` (métodos e variáveis de memória da classe).

## Arquivo de apoio (um por linguagem; a equipe envia só o seu arquivo)

| Linguagem | Arquivo da equipe | Apoio (no kit, no zip das fases e no servidor) | Fonte no orch |
| :--- | :--- | :--- | :--- |
| Python | `bot.py` (`from arena import *`) | `arena.py` | `wrappers/arena.py` |
| C | `bot.c` (`#include "arena.h"`) | `arena.h` | `wrappers/arena.h` |
| C++ | `bot.cpp` (`#include "arena.hpp"`) | `arena.hpp` | `wrappers/arena.hpp` |
| Java | `MeuBot.java` (`public class MeuBot extends Arena`) | `Arena.java` + `gson.jar` | `wrappers/Arena.java` |

As cópias do kit são iguais às do orch (ver `MANUTENCAO.md`).

## Assinaturas de `pensar`

| Linguagem | Assinatura |
| :--- | :--- |
| Python | `def pensar(estado):` devolve `Acao` |
| C | `Acao pensar(const Estado *e)` |
| C++ | `Acao pensar(const Estado& e)` |
| Java | `public static Acao pensar(Estado e)` |

## Estado (o que o tanque enxerga a cada frame)

| Campo | Tipo | Significado |
| :--- | :--- | :--- |
| `frame` | inteiro | número do frame (começa em 0) |
| `eu` | `Tanque` | o seu tanque |
| `inimigos` | lista de `Inimigo` | inimigos vivos (em C/Java também `n_inimigos`) |
| `perigos` | lista de `Perigo` | artilharia e laser (`n_perigos`) |
| `itens` | lista de `Item` | itens no mapa (`n_itens`) |
| `pontos` | lista de `Ponto` | pontos das fases de treino; no torneio, vazia (`n_pontos` = 0) |

Em Python, `estado.inimigos` etc. são listas (`len()`); em C e Java, vetores com `n_*`; em C++,
`std::vector` (`.size()`).

- `Tanque`: `id`, `x`, `y`, `vel_x`, `vel_y`, `angulo_chassi`, `angulo_torre`, `vida` (0 a 100),
  `energia` (0 a 100), `frames_para_atirar` (0 = pode atirar), `escudo_ativo`.
- `Inimigo`: `id`, `x`, `y`, `vel_x`, `vel_y` (sem a vida).
- `Perigo`: `id`, `tipo` (`PERIGO_ARTILHARIA` ou `PERIGO_LASER`), `x`, `y`, `raio`,
  `frames_ate_impacto` (0 = já ativo), `angulo` (feixe do laser), `frames_restantes`.
- `Item`: `id`, `tipo` (`ITEM_CURA` ou `ITEM_ENERGIA`), `x`, `y`.
- `Ponto`: `id` (texto: `"B"`, `"P1"`...), `x`, `y`, `raio`. Em Java compare com `p.id.equals("B")`;
  em C, `strcmp(p.id, "B") == 0`.

Ângulos em graus de 0 a 360; 0 aponta para +x e 90 para +y.

## Ação (o que o tanque faz neste frame)

| Campo | Valores | Efeito |
| :--- | :--- | :--- |
| `mover` | `FRENTE` (1), `PARADO` (0), `RE` (-1) ou qualquer valor de -1 a 1 | 5 unidades por frame na velocidade máxima, sem inércia |
| `direcao` | graus absolutos | para onde o chassi deve apontar; ele gira até 9 graus por frame até chegar |
| `angulo_torre` | graus absolutos | a torre aponta na hora |
| `atirar` | 1/0 ou true/false (Java: `boolean`) | atira se `frames_para_atirar == 0` e energia >= 20 (custo 20; espera 10 frames) |
| `ligar_escudo` | 1/0 ou true/false (Java: `boolean`) | liga o escudo neste frame |

O apoio converte `direcao` no `turn` da engine (o giro mais curto, limitado a 1) e `mover` no `throttle`.
O modelo preenche sempre os 5 campos, mantendo o chassi e a torre (`acao.direcao = meu.angulo_chassi`).


## Ajudantes de matemática (no arquivo da equipe)

| Função (Python/C/C++) | Java | Devolve |
| :--- | :--- | :--- |
| `distancia(x1, y1, x2, y2)` | `distancia(...)` | distância entre os dois pontos |
| `angulo_para(x1, y1, x2, y2)` | `angulo_para(...)` | ângulo de 0 a 360 de quem está em (x1, y1) olhando para (x2, y2) |
| `diferenca_angulo(de, para)` | `diferenca_angulo(...)` | giro mais curto, de -180 a 180 |

O `normalizar_angulo` saiu: a engine e o apoio aceitam qualquer ângulo, e `angulo_para` já devolve
0 a 360.

Os modelos de treino (`treino/NN_*/`) carregam o mesmo bloco de ajudantes do modelo principal da
linguagem. Depois de mudar os ajudantes, alinhe com:

    python3 empacotar_kit.py --alinhar-treino --fases ../battle-orchestrator/fases
