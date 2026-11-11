# Starter Kit - Game Jam PET 2026

Este kit traz um bot que já compila e anda pela arena, em quatro linguagens. A sua tarefa é escrever a função `pensar` do tanque. As regras da arena e do torneio estão no **enunciado do Desafio** (PDF da guia *Desafio* do BOCA). Os nomes dos campos do estado e da ação são os deste kit: estão comentados no arquivo de apoio de cada linguagem (`arena.py`, `arena.h`, `arena.hpp`, `Arena.java`) e resumidos no Início rápido abaixo.

## Conteúdo

| Pasta | Você edita e envia | Vem junto (não envie) |
| :--- | :--- | :--- |
| `c/` | `bot.c` | `arena.h` (tipos `Estado`, `Acao`, `Tanque`, `Inimigo`, `Perigo`, `Item`, `Ponto` e as constantes) |
| `cpp/` | `bot.cpp` | `arena.hpp` (os mesmos tipos, com `std::vector`) e `nlohmann/json.hpp` (usado pelo `arena.hpp`) |
| `java/` | `MeuBot.java` | `Arena.java` (os tipos e as constantes) e `gson.jar` (usado pelo `Arena.java`) |
| `python/` | `bot.py` | `arena.py` (os tipos e as constantes, `from arena import *`) |

Cada linguagem tem **um arquivo de apoio** (`arena.h`, `arena.hpp`, `Arena.java` ou `arena.py`). Ele já está no servidor: você envia só o seu arquivo. Abra o arquivo de apoio para ver, com comentários, todos os campos do estado e da ação.

Na raiz do kit ficam o `verificar.py` e a pasta `verificador/`: eles conferem o seu bot antes do envio (veja "Verificar antes de enviar"). A pasta `treino/` traz os modelos das fases da guia *Treino* (seção "Treino").

## Treino

Seis fases curtas na guia *Treino* do BOCA, em 3 blocos (movimento, mira, sobrevivência): cada uma ensina uma coisa e dá até 3 balões. Não vale ponto.

- `treino/<fase>/` tem o modelo da fase nas 4 linguagens, com um `TODO` escrito em passos numerados. O `treino/LEIA.md` explica o caminho.
- Complete o `TODO` e envie o arquivo na própria fase. O resultado e o replay aparecem lá.
- Os pontos da fase chegam em `estado.pontos` (C: `e->pontos[i]`, com `i < e->n_pontos`); os alvos, em `estado.inimigos`.
- Teste local: `python3 verificar.py treino/01_andar/bot.py --treino`.

## Início rápido

1. Escolha a linguagem e abra o arquivo da pasta dela.
2. Procure `SEU CÓDIGO COMEÇA AQUI`. O `pensar` do kit preenche os 5 campos da ação e traz um exemplo de estratégia em passos: acha o inimigo mais perto, aponta a torre, atira quando pode e anda.
3. Escreva a sua estratégia no lugar do exemplo.
4. Rode o verificador: `python3 verificar.py <pasta>/<arquivo>` (seção abaixo).
5. Envie o arquivo pela guia *Runs* do BOCA, escolhendo a linguagem certa.

Assinaturas de `pensar` (não podem mudar):

| Linguagem | Assinatura | Arquivo de apoio |
| :--- | :--- | :--- |
| C (C99) | `Acao pensar(const Estado *e)` | `#include "arena.h"` |
| C++20 | `Acao pensar(const Estado& e)` | `#include "arena.hpp"` |
| Java | `public static Acao pensar(Estado e)`, dentro de `public class MeuBot extends Arena` | `Arena.java` |
| Python 3 | `def pensar(estado):` (devolve uma `Acao()`) | `from arena import *` |

A ação tem 5 campos:

| Campo | O que é |
| :--- | :--- |
| `mover` | `FRENTE`, `PARADO` ou `RE`; qualquer valor de -1 a 1 também vale (0.5 = metade da velocidade) |
| `direcao` | para onde o chassi deve apontar, em graus (0 a 360); ele gira até 9 graus por frame até chegar lá |
| `angulo_torre` | para onde a torre aponta, em graus |
| `atirar` | sim (`True`/`true`/`1`) ou não |
| `ligar_escudo` | sim ou não (o escudo fica ligado só no frame em que você pede) |

Ângulos: 0 aponta para +x e 90 aponta para +y. Em Python, C++ e Java, `direcao` e `angulo_torre` não preenchidos mantêm o ângulo atual. **Em C**, preencha sempre os 5 campos: `Acao a = {0}` deixaria `direcao` e `angulo_torre` em 0 grau, e o tanque giraria para 0. Comece com `a.direcao = e->eu.angulo_chassi;` e `a.angulo_torre = e->eu.angulo_torre;`, como o kit faz.

## Verificar antes de enviar

Na pasta do kit:

```bash
python3 verificar.py python/bot.py      # ou c/bot.c, cpp/bot.cpp, java/MeuBot.java
python3 verificar.py c/bot.c --frames 600
python3 verificar.py treino/02_parar/bot.c --treino   # estados com os pontos do objetivo
```

O verificador faz, na sua máquina, o mesmo que o BOCA e a arena fazem com o seu arquivo:

| Etapa | O que confere | Com erro, no BOCA... |
| :--- | :--- | :--- |
| 1. Validação | As mesmas regras do validador: `main()`, assinatura do `pensar`, `package`, bibliotecas permitidas | o envio recebe Compilation Error |
| 2. Montagem | Compila o seu código junto com o código da arena, como na partida | o envio recebe Compilation Error |
| 3. Teste rodando | Executa o seu `pensar()` em 300 estados de jogo (um por frame): tempo de cada resposta, campos da ação, exceções e saída | o bot perde frames ou é eliminado na partida |

O que o teste rodando aponta:
- **Tempo:** a arena espera no máximo **50 ms** por frame. Um frame mais lento é perdido, e 20 seguidos eliminam o bot. O frame 0 tem 5 s, para o programa iniciar. Acima de 35 ms aparece um aviso: o servidor roda até 20 bots e pode ser mais lento que a sua máquina.
- **Exceção no `pensar()`:** a arena usa a ação parada naquele frame e o tanque fica parado. As primeiras linhas do erro aparecem no fim do relatório.
- **Campos da ação:** valor que não é número (ou `NaN`) é ignorado e vale o padrão (parado, sem tiro). `mover` fora de [-1, 1] é cortado para o limite.
- **Programa que termina, ou que não responde em 3 s:** na arena o bot seria desconectado e eliminado.

O teste rodando **não é uma partida**: os adversários andam em círculos e não atiram. Ele serve para achar erros e lentidão. Para ver a estratégia jogando, use o teste contra os NPCs na guia *Desafio* do BOCA.

O verificador precisa do Python 3.10+. As etapas 2 e 3 precisam do compilador da linguagem (`gcc`, `g++` ou `javac`) e do `bash`. No Windows, rode no WSL. Em Python, o teste rodando também funciona no Windows sem o `bash`.

## Compilar na sua máquina

Se quiser só compilar, sem o verificador, rode **dentro da pasta da linguagem**. Os comandos só conferem o código. Como o programa principal é o da arena, eles não geram um executável.

```bash
# C
gcc -std=c99 -Wall -I. -fsyntax-only bot.c

# C++
g++ -std=c++20 -Wall -I. -fsyntax-only bot.cpp

# Java (o servidor usa Java 17)
mkdir -p out && javac -cp gson.jar -d out Arena.java MeuBot.java

# Python (cria __pycache__/, que pode ser apagada)
python3 -m py_compile bot.py
```

## Abrir no VS Code

Use **Arquivo → Abrir Pasta**, não um arquivo solto. Abra a pasta que tem este `README.md` ou a pasta da sua linguagem (`c/`, `cpp/` ou `java/`): as duas trazem uma `.vscode/` que diz ao editor onde ficam o `arena.h`, o `arena.hpp` e o `gson.jar`. No Windows, o "Extrair Tudo" cria `starter_kit\starter_kit\`: abra a de **dentro**, senão o editor não lê a configuração e sublinha em vermelho tipos que existem, como `Estado` e `Acao`.

Extensões: *C/C++* (Microsoft) para C e C++, *Extension Pack for Java* para Java e *Python* para Python.

**C e C++ precisam de um compilador instalado**, até para o editor entender o código. Sem ele, a extensão não acha a biblioteca padrão e dá erros como estes, mesmo com o código certo:
- `cannot open source file "math.h"`;
- `std::vector ... has no member "push_back"`.

No Linux (como no laboratório), instale o `gcc`/`g++` pelo gerenciador de pacotes. No Windows, use uma destas opções:
- **WSL:** com a extensão *WSL*, rode "WSL: Abrir Pasta no WSL" e instale o `gcc`/`g++` lá (`sudo apt install build-essential`);
- **MSYS2/MinGW-w64:** instale o `gcc`/`g++` e escolha esse compilador em "C/C++: Select IntelliSense Configuration".

**Java precisa do JDK 17.** Se os erros em `Arena`, `Estado` ou `Acao` continuarem depois de abrir a pasta certa, rode o comando "Java: Clean Java Language Server Workspace" e recarregue a janela.

## Os ajudantes

No fim de cada arquivo há uma seção marcada:

```
AJUDANTES (opcional: use, mude ou apague)
```

São três funções de matemática, com ângulos em graus (0 aponta para +x; 90, para +y). Elas só calculam: nenhuma decide nada por você. É código seu: pode ler, mudar, renomear ou apagar.

| Ajudante | O que faz |
| :--- | :--- |
| `distancia(x1, y1, x2, y2)` | distância entre os dois pontos |
| `angulo_para(x1, y1, x2, y2)` | ângulo (0 a 360) de quem está em (x1, y1) olhando para (x2, y2) |
| `diferenca_angulo(de, para)` | quanto girar de um ângulo ao outro pelo caminho mais curto (-180 a 180) |

- Os nomes são os mesmos nas 4 linguagens.
- Em C e C++, os protótipos ficam logo depois dos `#include`, e as funções, no fim do arquivo. Em Java, os métodos ficam dentro da classe `MeuBot`, com `static`.
- Constantes (no arquivo de apoio): `FRENTE`, `PARADO`, `RE`, `PERIGO_ARTILHARIA`, `PERIGO_LASER`, `ITEM_CURA` e `ITEM_ENERGIA`. Compare sempre com a constante (`p.tipo == PERIGO_LASER`), não com um número: em Python elas são textos, nas outras linguagens são números.
- **Java:** o mais simples é criar tudo (métodos, variáveis e classes auxiliares) **dentro** da classe `MeuBot`. O `pensar` precisa estar na classe pública do arquivo.

## Envio pela guia Runs

- Envie **um único arquivo** (`bot.c`, `bot.cpp`, `MeuBot.java` ou `bot.py`), com a linguagem certa selecionada.
- **YES**: o código compila exatamente como vai rodar na partida e passa a ser a sua **versão ativa**, a que entra nas rodadas.
- **Compilation Error**: o motivo aparece no botão *Ver Erro*. A versão ativa anterior continua valendo.
- Para testar sem enviar, use o teste da guia *Desafio* (versão ativa ou arquivo avulso, contra os adversários de um ponto de checagem).

## Problemas comuns

O motivo de um Compilation Error aparece no botão *Ver Erro*, sem acentos (de propósito). Nos casos reconhecidos, vem uma linha `ERRO DE VALIDACAO: ...`. Nos demais, vem `ERRO DE COMPILACAO: o compilador recusou o seu codigo.`, seguida da saída do compilador (em Python, `erro de sintaxe na linha N: ...`). Comentários não contam.

| Mensagem (início) | Linguagem | O que fazer |
| :--- | :--- | :--- |
| `... pensar ... nao foi encontrada` / `nao foi encontrado` | todas | Defina `pensar` com a assinatura da tabela acima (em Python, no nível do arquivo, sem recuo). |
| `a assinatura de pensar esta errada` | C, C++ | Use exatamente a assinatura do kit (com `const`). |
| `a funcao 'Acao pensar(const Estado *e)' nao esta definida` | C | Escreva o corpo da função (não basta declará-la). |
| `o metodo pensar esta errado ou fora da classe principal` | Java | `public static Acao pensar(Estado e)`, dentro da classe pública do arquivo (`public class MeuBot extends Arena`). |
| `a classe do seu bot nao pode se chamar Arena` | Java | Use outro nome, por exemplo `MeuBot`. |
| `o campo 'hp' agora se chama vida` (ou outro campo) | C, C++, Java | O campo tem um nome novo, em português: troque pelo nome que a mensagem indica. Todos estão no arquivo de apoio. |
| `nao crie a funcao main()` | C, C++ | O programa principal é o da arena: apague a sua `main`. (Em Java, um `main` a mais é ignorado.) |
| `remova a linha 'package'` | Java | Envie um único arquivo, sem `package`. |
| `a biblioteca externa '...' nao e permitida` | Python | Só a biblioteca padrão (`math`, `random`, `collections`, `heapq`...) e o `arena`. numpy não existe no servidor, e outros arquivos seus também não: só um arquivo é enviado. |
| `import relativo ... nao e permitido` | Python | Mantenha todo o código num único arquivo. |
| `remova o bloco "if __name__ == '__main__':"` | Python | Apague o bloco: a arena já chama `pensar(estado)`. |
| `input() no nivel do arquivo` / `sys.stdin ... nao pode ser usado` | Python | Não leia a entrada: o estado chega como argumento de `pensar`. |
| `o modulo 'os' nao e permitido`, `o uso de eval() ...`, `uso de funcoes de sistema (system)`, `chamada de execucao de sistema` | todas | Recursos de sistema são proibidos (Regulamento, item 10.3): `os`, `subprocess`, `importlib`, `eval`, `exec` e `__import__` em Python; `system` em C/C++; `Runtime.getRuntime`, `ProcessBuilder` e `System.exit` em Java. |
| `o #include "..." (linha N) nao e permitido` | C, C++ | Use só bibliotecas padrão e os arquivos do kit (`arena.h`, `arena.hpp`). |
| `ERRO DE COMPILACAO` com `undefined reference to 'distancia'` | C | As funções de matemática não estão no `arena.h`: mantenha (ou copie) as da seção de ajudantes do `bot.c`. |
| `Timeout de compilação excedido (60s)` | todas | Simplifique macros, templates ou includes pesados. |

| Outros problemas | Causa e solução |
| :--- | :--- |
| Em C, o tanque ou a torre viram para 0 grau sozinhos | Em C os 5 campos da ação são sempre enviados. Comece de `a.direcao = e->eu.angulo_chassi;` e `a.angulo_torre = e->eu.angulo_torre;`. |
| O tanque não atira | Atirar precisa de `frames_para_atirar == 0` e `energia >= 20`. O escudo gasta energia a cada frame ligado. |
| `print`/`printf`/`System.out` não aparece | A saída padrão é do executor e vai para um log descartado. Depure na sua máquina (com o `verificar.py`) ou pelo visualizador. |
| `[AVISO]` no log do treino ("Avisos do seu código") | O bot funcionou, mas usou um nome antigo de campo da ação ou um valor que não é número. O aviso diz o que trocar. |
| O tanque some no meio da partida | Cada resposta tem 50 ms. 20 frames seguidos sem resposta, ou o programa encerrado (`exit`, erro fatal), eliminam o tanque. Evite laços pesados a cada frame. |

## Visualizador (Linux)

Depois de um teste na guia *Desafio*, baixe o visualizador da partida e, no terminal:

```bash
unzip <arquivo>.zip
cd GameJam_Arena
chmod +x Unity-Build-Linux.x86_64
./Unity-Build-Linux.x86_64
```
