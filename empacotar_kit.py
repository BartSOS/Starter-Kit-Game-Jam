#!/usr/bin/env python3
"""
Gera o starter_kit.zip das equipes a partir desta pasta (fonte única do zip).

Zip determinístico: entradas ordenadas, data fixa, permissões 0644 e create_system Unix,
sob a pasta raiz starter_kit/. Ficam de fora os arquivos internos da organização
(AJUDANTES.md, ERROS_VALIDADOR.md, MANUTENCAO.md e este script), os ocultos (menos a
configuração do VS Code em .vscode/) e os caches.

Quem usa:
  - o build da imagem web do Boca-Game-Jam-Pet (Dockerfile, estágio dist);
  - a skill boca-desafio (desafio.py --starter e --conferir importam este módulo).

Uso:
    python3 empacotar_kit.py --saida starter_kit.zip [--pasta DIR]
    python3 empacotar_kit.py --alinhar-treino [--fases ../battle-orchestrator/fases]
Só a biblioteca padrão. Código 1 se faltar algum arquivo obrigatório ou se a seção
AJUDANTES de um modelo de treino/ divergir da do modelo principal da linguagem.
"""

import argparse
import os
import sys
import zipfile

PASTA_RAIZ_ZIP = "starter_kit"
DATA_FIXA = (2026, 1, 1, 0, 0, 0)  # datas fixas: o mesmo kit gera o mesmo zip
EXCLUIDOS = {"AJUDANTES.md", "ERROS_VALIDADOR.md", "MANUTENCAO.md", "empacotar_kit.py"}
# Ocultos que vão no zip: a configuração do VS Code (acha o arena.h, o json.hpp e o gson.jar)
OCULTOS_PERMITIDOS = {".vscode"}
OBRIGATORIOS = [
    "README.md",
    ".vscode/c_cpp_properties.json", ".vscode/settings.json",
    "c/.vscode/c_cpp_properties.json", "cpp/.vscode/c_cpp_properties.json", "java/.vscode/settings.json",
    "c/bot.c", "c/arena.h",
    "cpp/bot.cpp", "cpp/nlohmann/json.hpp",
    "java/MeuBot.java", "java/gson.jar",
    "python/bot.py",
    # Verificador: as mesmas checagens e a mesma montagem da partida (cópias do battle-orchestrator)
    "verificar.py",
    "verificador/build_bot.sh", "verificador/checar_fonte.py", "verificador/checar_python.py",
    "verificador/wrapper.py", "verificador/wrapper.java", "verificador/cpp_header.hpp",
    "verificador/cpp_footer.cpp", "verificador/c_wrapper.cpp",
]

# Treino: um modelo por fase e linguagem. Os ids são os de battle-orchestrator/fases/*.json
# (--fases confere). A seção AJUDANTES de cada modelo é cópia da do modelo principal da
# linguagem: o zip não sai se divergir (--alinhar-treino recopia).
FASES_TREINO = ["01_andar", "02_parar", "03_percurso", "04_mira_parado", "05_mira_andando", "06_artilharia"]
MODELOS = {"bot.py": "python/bot.py", "bot.c": "c/bot.c", "bot.cpp": "cpp/bot.cpp", "MeuBot.java": "java/MeuBot.java"}
OBRIGATORIOS += ["treino/LEIA.md"] + [f"treino/{f}/{n}" for f in FASES_TREINO for n in MODELOS]


def secao_ajudantes(texto):
    """(início, fim) da seção AJUDANTES em linhas: da moldura antes de 'AJUDANTES (opcional'
    até a moldura depois de 'FIM DOS AJUDANTES', inclusive. None se faltar um marcador."""
    linhas = texto.split("\n")
    ini = next((i for i, l in enumerate(linhas) if "AJUDANTES (opcional" in l), None)
    fim = next((i for i, l in enumerate(linhas) if "FIM DOS AJUDANTES" in l), None)
    if ini is None or fim is None or ini < 1 or fim + 1 >= len(linhas) or fim < ini:
        return None
    return ini - 1, fim + 1


def _ler(caminho):
    with open(caminho, encoding="utf-8", newline="") as f:
        return f.read()


def _ajudantes(texto):
    s = secao_ajudantes(texto)
    return None if s is None else "\n".join(texto.split("\n")[s[0]:s[1] + 1])


def treino_desalinhado(pasta, alinhar=False):
    """Modelos de treino cuja seção AJUDANTES difere da do modelo principal (com alinhar=True, recopia)."""
    ruins = []
    for fase in FASES_TREINO:
        for nome, principal in MODELOS.items():
            alvo = os.path.join(pasta, "treino", fase, nome)
            if not os.path.isfile(alvo) or not os.path.isfile(os.path.join(pasta, principal)):
                continue
            certo, texto = _ajudantes(_ler(os.path.join(pasta, principal))), _ler(alvo)
            s = secao_ajudantes(texto)
            if certo is None or s is None:
                ruins.append(f"treino/{fase}/{nome}")  # sem marcadores: não dá para alinhar
            elif _ajudantes(texto) == certo:
                continue
            elif alinhar:
                linhas = texto.split("\n")
                novo = "\n".join(linhas[:s[0]] + certo.split("\n") + linhas[s[1] + 1:])
                with open(alvo, "w", encoding="utf-8", newline="") as f:
                    f.write(novo)
            else:
                ruins.append(f"treino/{fase}/{nome}")
    return ruins


def ignorado(nome):
    """Nomes que nunca entram no zip: ocultos (menos o .vscode), caches Python e os arquivos internos."""
    return ((nome.startswith(".") and nome not in OCULTOS_PERMITIDOS) or nome == "__pycache__" or nome in EXCLUIDOS
            or nome.endswith((".pyc", ".pyo")))


def listar_kit(pasta):
    """Arquivos do kit a empacotar, como [(caminho relativo com /, caminho absoluto)], em ordem."""
    arquivos = []
    for raiz, dirs, nomes in os.walk(pasta):
        dirs[:] = [d for d in dirs if not ignorado(d)]
        for nome in nomes:
            absoluto = os.path.join(raiz, nome)
            if ignorado(nome) or os.path.islink(absoluto):
                continue
            rel = os.path.relpath(absoluto, pasta).replace(os.sep, "/")
            arquivos.append((rel, absoluto))
    return sorted(arquivos)


def faltando(presentes):
    """Obrigatórios que não estão no conjunto de caminhos relativos."""
    return [r for r in OBRIGATORIOS if r not in presentes]


def gravar_zip(destino, arquivos):
    """Grava o zip de forma atômica (temporário + os.replace)."""
    pasta = os.path.dirname(os.path.abspath(destino))
    os.makedirs(pasta, exist_ok=True)
    tmp = destino + ".tmp"
    try:
        with zipfile.ZipFile(tmp, "w") as zf:
            for rel, absoluto in arquivos:
                info = zipfile.ZipInfo(f"{PASTA_RAIZ_ZIP}/{rel}", date_time=DATA_FIXA)
                info.create_system = 3
                info.external_attr = 0o644 << 16
                info.compress_type = zipfile.ZIP_DEFLATED
                with open(absoluto, "rb") as f:
                    zf.writestr(info, f.read())
        os.replace(tmp, destino)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


def empacotar(pasta, saida):
    """Gera o zip. Devolve (código, mensagem)."""
    pasta = os.path.abspath(pasta)
    if not os.path.isdir(pasta):
        return 1, f"ERRO pasta do kit não existe: {pasta}"
    arquivos = listar_kit(pasta)
    falta = faltando({rel for rel, _ in arquivos})
    if falta:
        return 1, "ERRO kit incompleto, zip não gerado. Faltam: " + ", ".join(falta)
    ruins = treino_desalinhado(pasta)
    if ruins:
        return 1, ("ERRO ajudantes do treino diferentes dos modelos principais (rode --alinhar-treino): "
                   + ", ".join(ruins))
    gravar_zip(saida, arquivos)
    return 0, f"OK zip: {len(arquivos)} arquivos -> {saida}"


def main():
    ap = argparse.ArgumentParser(description="Gera o starter_kit.zip das equipes.")
    ap.add_argument("--saida", help="caminho do zip a gerar")
    ap.add_argument("--pasta", default=os.path.dirname(os.path.abspath(__file__)),
                    help="pasta do kit (padrão: a deste script)")
    ap.add_argument("--alinhar-treino", action="store_true",
                    help="recopia a seção AJUDANTES dos modelos principais para treino/*/")
    ap.add_argument("--fases", metavar="DIR", help="confere FASES_TREINO com DIR/*.json (battle-orchestrator/fases)")
    args = ap.parse_args()
    if args.alinhar_treino or args.fases:
        codigo = 0
        if args.alinhar_treino:
            ruins = treino_desalinhado(os.path.abspath(args.pasta), alinhar=True)
            print("ERRO sem marcadores AJUDANTES: " + ", ".join(ruins) if ruins else "OK treino alinhado")
            codigo = 1 if ruins else 0
        if args.fases:
            ids = sorted(n[:-5] for n in os.listdir(args.fases) if n.endswith(".json"))
            igual = ids == sorted(FASES_TREINO)
            print("OK fases do treino = fases do orch" if igual else f"ERRO fases do orch {ids} != FASES_TREINO")
            codigo = codigo or (0 if igual else 1)
        return codigo
    if not args.saida:
        ap.error("--saida é obrigatório")
    codigo, msg = empacotar(args.pasta, args.saida)
    print(msg)
    return codigo


if __name__ == "__main__":
    sys.exit(main())
