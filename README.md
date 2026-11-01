# Starter Kit - Game Jam PET 2026

Este kit traz um bot que já compila e anda pela arena, em quatro linguagens. A sua tarefa é escrever a função `pensar` do tanque. As regras completas (estado, ação, arena e torneio) estão no **enunciado do Desafio** (PDF da guia *Desafio* do BOCA).

## Conteúdo

| Pasta | Você edita e envia | Vem junto (não envie) |
| :--- | :--- | :--- |
| `c/` | `bot.c` | `arena.h` (tipos `Estado`, `Acao`, `Tanque`, `Inimigo`, `Hazard`, `Item`, `Ponto`) |
| `cpp/` | `bot.cpp` | `nlohmann/json.hpp` (biblioteca JSON) |
| `java/` | `MeuBot.java` | `gson.jar` (biblioteca Gson) |
| `python/` | `bot.py` | nada: só a biblioteca padrão do Python 3 |

Na raiz do kit ficam o `verificar.py` e a pasta `verificador/`: eles conferem o seu bot antes do envio (veja "Verificar antes de enviar"). A pasta `treino/` traz os modelos das fases da guia *Treino* (seção "Treino").

## Treino

Seis fases curtas na guia *Treino* do BOCA, em 3 blocos (movimento, mira, sobrevivência): cada uma ensina uma coisa e dá até 3 balões. Não vale ponto.

- `treino/<fase>/` tem o modelo da fase nas 4 linguagens, com um único `TODO`.
- Complete o `TODO` e envie o arquivo na própria fase. O resultado e o replay aparecem lá.
- Os pontos da fase chegam em `estado["objetivo"]["pontos"]` (C: `e->pontos[i]`, `i < e->n_pontos`); os alvos, em `enemies`.
- Teste local: `python3 verificar.py treino/01_andar/bot.py --treino`.

## Início rápido

1. Escolha a linguagem e abra o arquivo da pasta dela.
2. Procure `SEU CÓDIGO COMEÇA AQUI`, logo depois da seção de ajudantes. O `pensar` do kit lê todos os campos do estado, com um comentário em cada um, e devolve uma ação simples: andar para a frente girando devagar, sem atirar.
3. Escreva a sua estratégia no lugar da ação simples.
4. Rode o verificador: `python3 verificar.py <pasta>/<arquivo>` (seção abaixo).
5. Envie o arquivo pela guia *Runs* do BOCA, escolhendo a linguagem certa.

Assinaturas de `pensar` (não podem mudar):

| Linguagem | Assinatura |
| :--- | :--- |
| C (C99) | `Acao pensar(const Estado *e)` |
| C++20 | `json pensar(const json& estado)` |
| Java | `public static JsonObject pensar(JsonObject estado)` |
| Python 3 | `def pensar(estado):` (recebe e devolve um `dict`) |

## Verificar antes de enviar

Na pasta do kit:

```bash
python3 verificar.py python/bot.py      # ou c/bot.c, cpp/bot.cpp, java/MeuBot.java
python3 verificar.py c/bot.c --ticks 600
python3 verificar.py treino/02_parar/bot.c --treino   # estados com os pontos do objetivo
```

O verificador faz, na sua máquina, o mesmo que o BOCA e a arena fazem com o seu arquivo:

| Etapa | O que confere | Com erro, no BOCA... |
| :--- | :--- | :--- |
| 1. Validação | As mesmas regras do validador: `main()`, assinatura do `pensar`, `package`, bibliotecas permitidas | o envio recebe Compilation Error |
| 2. Montagem | Compila o seu código junto com o código da arena, como na partida | o envio recebe Compilation Error |
| 3. Teste rodando | Executa o seu `pensar()` em 300 estados de jogo: tempo de cada resposta, campos da ação, exceções e saída | o bot perde ticks ou é eliminado na partida |

O que o teste rodando aponta:
- **Tempo:** a arena espera no máximo **50 ms** por tick. Um tick mais lento é perdido, e 20 seguidos eliminam o bot. O tick 0 tem 5 s, para o programa iniciar. Acima de 35 ms aparece um aviso: o servidor roda até 20 bots e pode ser mais lento que a sua máquina.
- **Exceção no `pensar()`:** a arena usa a ação parada (`{}`) naquele tick e o tanque fica parado. As primeiras linhas do erro aparecem no fim do relatório.
- **Campos da ação:** `throttle`, `turn` e `turret_angle` são números; `shoot` e `shield` são `true`/`false`. Campo com tipo errado, `NaN` ou nulo é ignorado e vale o padrão (parado, sem tiro). Número em `shoot`/`shield` é aceito (diferente de 0 = sim), com aviso. `throttle`/`turn` fora de [-1, 1] são cortados para o limite.
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
mkdir -p out && javac -cp gson.jar -d out MeuBot.java

# Python (cria __pycache__/, que pode ser apagada)
python3 -m py_compile bot.py
```

O template gera avisos de "variável não usada" com `-Wall`, porque lê todos os campos só para mostrar o que existe. Eles somem quando você passa a usar os valores.

## Abrir no VS Code

Use **Arquivo → Abrir Pasta**, não um arquivo solto. Abra a pasta que tem este `README.md` ou a pasta da sua linguagem (`c/`, `cpp/` ou `java/`): as duas trazem uma `.vscode/` que diz ao editor onde ficam o `arena.h`, o `nlohmann/json.hpp` e o `gson.jar`. No Windows, o "Extrair Tudo" cria `starter_kit\starter_kit\`: abra a de **dentro**, senão o editor não lê a configuração e sublinha em vermelho tipos que existem, como `Estado`, `json` e `JsonObject`.

Extensões: *C/C++* (Microsoft) para C e C++, *Extension Pack for Java* para Java e *Python* para Python.

**C e C++ precisam de um compilador instalado**, até para o editor entender o código. Sem ele, a extensão não acha a biblioteca padrão e dá erros como estes, mesmo com o código certo:
- `cannot open source file "math.h"`;
- `no instance of constructor ... basic_json`;
- `std::vector ... has no member "push_back"`.

No Linux (como no laboratório), instale o `gcc`/`g++` pelo gerenciador de pacotes. No Windows, use uma destas opções:
- **WSL:** com a extensão *WSL*, rode "WSL: Abrir Pasta no WSL" e instale o `gcc`/`g++` lá (`sudo apt install build-essential`);
- **MSYS2/MinGW-w64:** instale o `gcc`/`g++` e escolha esse compilador em "C/C++: Select IntelliSense Configuration".

**Java precisa do JDK 17.** Se os erros em `import com.google.gson...` continuarem depois de abrir a pasta certa, rode o comando "Java: Clean Java Language Server Workspace" e recarregue a janela.

## Os ajudantes

No topo de cada arquivo há uma seção marcada:

```
AJUDANTES (opcional: renomeie, altere ou apague)
```

Ela **só facilita o acesso aos dados**: nenhum ajudante decide nada por você. É código seu: pode ler, mudar, renomear ou apagar.

| Ajudante | Python / C++ | Java | O que faz |
| :--- | :--- | :--- | :--- |
| acessores | `tick`, `eu`, `inimigos`, `perigos`, `itens` | iguais | leem o estado e devolvem objetos (`Tanque`, `Inimigo`, `Hazard`, `Item`) |
| montador | `montar_acao(throttle, turn, turret_angle, shoot, shield)` | `montarAcao(...)` | monta a ação com os tipos certos; a torre é opcional (Python: `None`; C++ e Java: variante sem o parâmetro) |
| matemática | `distancia`, `angulo_para`, `diferenca_angulo`, `normalizar_angulo` | `distancia`, `anguloPara`, `diferencaAngulo`, `normalizarAngulo` | distância e ângulos em graus (0 = +x, crescendo de +x para +y) |

- Os campos têm os mesmos nomes do estado: `x`, `y`, `vx`, `vy`, `angle`, `turret_angle`, `hp`, `energy`, `cooldown` e `shield` (em Java, `turretAngle`). `eu(estado).hp` é o mesmo valor de `estado["self"]["hp"]`.
- Constantes: `HAZARD_ARTILHARIA = 0`, `HAZARD_LASER = 1`, `ITEM_CURA = 0`, `ITEM_ENERGIA = 1`.
- **Em C** o estado já chega tipado (`e->tick`, `e->self`, `e->inimigos[i]` com `i < e->n_inimigos`, `e->hazards[i]`, `e->itens[i]`), então só há as funções de matemática e comentários.
- **Para apagar os ajudantes:** remova a seção inteira, entre as linhas marcadas `AJUDANTES` e `FIM DOS AJUDANTES`, e leia o estado bruto (`dict` em Python, `json` em C++, `JsonObject` em Java). Em Java, apague também os `import` que ficarem sem uso (opcional). Para renomear um ajudante, troque o nome na definição e em todos os usos.
- **Java:** o mais simples é criar tudo (métodos e classes auxiliares) **dentro** da classe `MeuBot`, como as classes aninhadas do kit. O `pensar` precisa estar na classe pública do arquivo.

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
| `o metodo pensar esta errado ou fora da classe principal` | Java | `public static JsonObject pensar(JsonObject estado)`, dentro da classe pública do arquivo. |
| `nao crie a funcao main()` | C, C++ | O programa principal é o da arena: apague a sua `main`. (Em Java, um `main` a mais é ignorado.) |
| `remova a linha 'package'` | Java | Envie um único arquivo, sem `package`. |
| `a biblioteca externa '...' nao e permitida` | Python | Só a biblioteca padrão (`math`, `random`, `collections`, `heapq`...). numpy não existe no servidor, e outros arquivos seus também não: só um arquivo é enviado. |
| `import relativo ... nao e permitido` | Python | Mantenha todo o código num único arquivo. |
| `remova o bloco "if __name__ == '__main__':"` | Python | Apague o bloco: a arena já chama `pensar(estado)`. |
| `input() no nivel do arquivo` / `sys.stdin ... nao pode ser usado` | Python | Não leia a entrada: o estado chega como argumento de `pensar`. |
| `o modulo 'os' nao e permitido`, `o uso de eval() ...`, `uso de funcoes de sistema (system)`, `chamada de execucao de sistema` | todas | Recursos de sistema são proibidos (Regulamento, item 10.3): `os`, `subprocess`, `importlib`, `eval`, `exec` e `__import__` em Python; `system` em C/C++; `Runtime.getRuntime`, `ProcessBuilder` e `System.exit` em Java. |
| `o #include "..." (linha N) nao e permitido` | C, C++ | Use só bibliotecas padrão e os arquivos do kit (`arena.h`, `nlohmann/json.hpp`). |
| `ERRO DE COMPILACAO` com `undefined reference to 'distancia'` | C | As funções de matemática não estão no `arena.h`: mantenha (ou copie) as da seção de ajudantes do `bot.c`. |
| `Timeout de compilação excedido (60s)` | todas | Simplifique macros, templates ou includes pesados. |

| Outros problemas | Causa e solução |
| :--- | :--- |
| O tanque fica parado ou não atira | Confira os tipos: `shoot` e `shield` precisam ser booleanos, e `throttle`, `turn` e `turret_angle`, números. Com tipo errado, a arena ignora o tick inteiro. Use o montador. |
| Em C, a torre vira para 0° sozinha | Em C a torre é sempre enviada. Comece de `a.turret_angle = e->self.turret_angle`. |
| `print`/`printf`/`System.out` não aparece | A saída padrão é do executor e vai para um log descartado. Depure na sua máquina ou pelo visualizador. |
| O tanque some no meio da partida | Cada resposta tem 50 ms. 20 ticks seguidos sem resposta, ou o programa encerrado (`exit`, erro fatal), eliminam o tanque. Evite laços pesados a cada tick. |

## Visualizador (Linux)

Depois de um teste na guia *Desafio*, baixe o visualizador da partida e, no terminal:

```bash
unzip <arquivo>.zip
cd GameJam_Arena
chmod +x Unity-Build-Linux.x86_64
./Unity-Build-Linux.x86_64
```
