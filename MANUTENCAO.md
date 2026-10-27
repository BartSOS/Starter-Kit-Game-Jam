# Manutenção do Starter Kit (organização)

Material interno: este arquivo, o `AJUDANTES.md` e o `ERROS_VALIDADOR.md` **não vão** no zip das equipes. O `README.md` é o das equipes e vai no zip.

Repositório privado `BartSOS/Starter-Kit-Game-Jam`. No workspace, fica em `Docker/Starter-Kit-Game-Jam/`, ao lado do `battle-orchestrator/`. Até 27/10/2026 o kit ficava em `battle-orchestrator/starter-kit/`, e o histórico veio junto.

## Arquivos copiados do orchestrator
Três arquivos são cópias do `battle-orchestrator`, que é a fonte, e precisam ficar iguais ao que a partida usa:

| Kit | Origem no orchestrator |
| :--- | :--- |
| `c/arena.h` | `wrappers/arena.h` |
| `cpp/nlohmann/json.hpp` | `engine/nlohmann/json.hpp` |
| `java/gson.jar` | `libs/gson-2.10.1.jar` |

No WSL, a partir da raiz do workspace:
```bash
bash battle-orchestrator/empacotar.sh --conferir-kit      # código 1 se alguma cópia divergir
bash battle-orchestrator/empacotar.sh --sincronizar-kit   # copia de novo para este repositório
```
O caminho do kit vem de `GAMEJAM_KIT_DIR` (padrão `../Starter-Kit-Game-Jam`, relativo ao orchestrator).

## Ajudantes e validador
- `AJUDANTES.md`: nomes e assinaturas dos ajudantes, iguais nas 4 linguagens.
- `ERROS_VALIDADOR.md`: texto exato de cada Compilation Error do validador.

Mudou um ajudante? Atualize os 4 arquivos e o `AJUDANTES.md`. O `testar_kits.py` confere se os valores batem entre as linguagens, se os NPCs e o espelho `bots_base` usam os mesmos ajudantes, e se cada template recebe YES e joga.

## Gerar e publicar o zip
```bash
python3 .claude/skills/boca-desafio/scripts/desafio.py --starter     # gera mock-data/assets/starter_kit.zip
python3 .claude/skills/boca-desafio/scripts/desafio.py --conferir    # confere os obrigatórios
python3 .claude/skills/boca-gerenciar-engine/scripts/testar_kits.py  # templates, ajudantes e NPCs
```
O zip é determinístico: o mesmo kit gera o mesmo arquivo. Ele fica versionado no `Boca-Game-Jam-Pet` (`boca-docker/qa-suite/mock-data/assets/`) e entra na imagem do GHCR a partir de lá. Por isso, depois de mudar o kit, gere o zip, faça commit no Boca-Game-Jam-Pet e publique as imagens.
