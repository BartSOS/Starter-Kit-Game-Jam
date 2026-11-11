# Treino

Um modelo por fase, nas 4 linguagens (`bot.py`, `bot.c`, `bot.cpp`, `MeuBot.java`).
Cada modelo traz no topo as regras da fase e, dentro do `pensar()`, os `TODO` em passos
numerados (PASSO 1, PASSO 2...): só o que a fase ensina falta fazer.

1. Abra a fase na guia **Treino** do BOCA e leia o objetivo.
2. Baixe o zip da fase na sua linguagem (ou use a pasta da fase aqui) e complete os passos.
3. Envie o arquivo na própria fase. Veja o resultado e o replay, ajuste e envie de novo.

O que o modelo usa:

- os pontos da fase ficam em `estado.pontos` (em C e C++: `e->pontos`, `e->n_pontos`;
  em Java: `e.pontos`, `e.n_pontos`); cada ponto tem `id` ("B", ou "P1" a "P4"), `x`, `y` e `raio`;
- os alvos das fases de mira ficam em `inimigos`; a artilharia da fase 06, em `perigos`;
- o tempo é contado em frames (`estado.frame`); o tanque anda 5 unidades por frame.

Fora do treino não há pontos, e o modelo fica parado. Treino não vale ponto: até 3 balões por fase.

As mensagens que o seu bot escreve com `print` (Python), `fprintf(stderr, ...)` (C),
`cerr` (C++) ou `System.err.println` (Java) não aparecem no resultado da fase. Para ver o
que o seu bot faz, use o replay ou o teste local:

    python3 verificar.py treino/01_andar/bot.py --treino

Java no VS Code: copie o `MeuBot.java` da fase para `java/` (no lugar do modelo principal) e
edite lá, onde o `gson.jar` já está configurado. No zip da fase o `gson.jar` já vem junto.
