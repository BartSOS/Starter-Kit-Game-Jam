# Treino

Um modelo por fase, nas 4 linguagens. Cada um tem um único `TODO`: o ponto que a fase ensina.

1. Abra a fase na guia **Treino** do BOCA e leia o objetivo.
2. Complete o `TODO` do modelo da fase (ex.: `01_andar/bot.py`).
3. Envie o arquivo na própria fase. Veja o resultado e o replay, ajuste, envie de novo.

Os pontos da fase chegam em `estado["objetivo"]["pontos"]` (em C: `e->pontos`, `e->n_pontos`); os alvos, em `enemies`.
Fora do treino essa chave não existe e o modelo fica parado. Treino não vale ponto: 3 balões por fase.

Teste local: `python3 verificar.py treino/01_andar/bot.py --treino`
