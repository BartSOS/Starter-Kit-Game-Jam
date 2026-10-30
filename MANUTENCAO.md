# Manutenção do Starter Kit (organização)

Material interno: este arquivo, o `AJUDANTES.md` e o `ERROS_VALIDADOR.md` **não vão** no zip das equipes. O `README.md` é o das equipes e vai no zip.

Repositório privado `BartSOS/Starter-Kit-Game-Jam`. No workspace, fica em `Docker/Starter-Kit-Game-Jam/`, ao lado do `battle-orchestrator/`. Até 27/10/2026 o kit ficava em `battle-orchestrator/starter-kit/`, e o histórico veio junto.

## Arquivos copiados do orchestrator
Estes arquivos são cópias do `battle-orchestrator`, que é a fonte, e precisam ficar iguais ao que a partida usa:

| Kit | Origem no orchestrator |
| :--- | :--- |
| `c/arena.h` | `wrappers/arena.h` |
| `cpp/nlohmann/json.hpp` | `engine/nlohmann/json.hpp` |
| `java/gson.jar` | `libs/gson-2.10.1.jar` |
| `verificador/build_bot.sh`, `checar_fonte.py`, `checar_python.py` | `wrappers/` (mesmos nomes) |
| `verificador/wrapper.py`, `wrapper.java`, `cpp_header.hpp`, `cpp_footer.cpp`, `c_wrapper.cpp` | `wrappers/` (mesmos nomes) |

A pasta `verificador/` é o que o `verificar.py` usa para montar e rodar o bot igual à partida. Nunca edite essas cópias aqui: mude no orch e sincronize.

No WSL, a partir da raiz do workspace:
```bash
bash battle-orchestrator/empacotar.sh --conferir-kit      # código 1 se alguma cópia divergir
bash battle-orchestrator/empacotar.sh --sincronizar-kit   # copia de novo para este repositório
python3 .claude/skills/boca-gerenciar-engine/scripts/testar_kits.py --copias   # confere estas e as outras cópias do workspace
```
O caminho do kit vem de `GAMEJAM_KIT_DIR` (padrão `../Starter-Kit-Game-Jam`, relativo ao orchestrator).

## Ajudantes e validador
- `AJUDANTES.md`: nomes e assinaturas dos ajudantes, iguais nas 4 linguagens.
- `ERROS_VALIDADOR.md`: texto exato de cada Compilation Error do validador.

Mudou um ajudante? Atualize os 4 arquivos e o `AJUDANTES.md`. O `testar_kits.py` confere se os valores batem entre as linguagens, se os NPCs e o espelho `bots_base` usam os mesmos ajudantes, e se cada template recebe YES e joga.

## O zip das equipes
O `empacotar_kit.py`, neste repositório, é a **fonte única** do `starter_kit.zip`. Ele usa só a biblioteca padrão. O zip é determinístico:
- entradas em ordem;
- data fixa;
- pasta raiz `starter_kit/`;
- de fora: os arquivos internos (este, o `AJUDANTES.md`, o `ERROS_VALIDADOR.md` e o próprio script).

Quem o usa:
- **o build da imagem** (GHCR), que faz checkout deste repositório (secret `KIT_TOKEN`), gera o zip na hora e registra o commit do kit no `manifest.json`. Nada do kit fica versionado no Boca-Game-Jam-Pet;
- **a skill `boca-desafio`**, que importa este módulo;
- **o `test_orchestrator.py`**, que gera o zip a cada simulação.

```bash
python3 Starter-Kit-Game-Jam/empacotar_kit.py --saida /tmp/starter_kit.zip  # direto
python3 .claude/skills/boca-desafio/scripts/desafio.py --starter            # mock-data/assets/starter_kit.zip (local, fora do git)
python3 .claude/skills/boca-desafio/scripts/desafio.py --conferir           # obrigatórios, proibidos e o PDF
python3 .claude/skills/boca-gerenciar-engine/scripts/testar_kits.py         # templates, ajudantes e NPCs
```
Mudou o kit? Commit e push aqui, depois publique as imagens. Um push neste repositório não dispara a publicação: rode o workflow do Boca-Game-Jam-Pet manualmente ou crie uma tag `v*`.
