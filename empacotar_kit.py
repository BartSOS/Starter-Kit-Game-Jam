#!/usr/bin/env python3
"""
Gera o starter_kit.zip das equipes a partir desta pasta (fonte única do zip).

Zip determinístico: entradas ordenadas, data fixa, permissões 0644 e create_system Unix,
sob a pasta raiz starter_kit/. Ficam de fora os arquivos internos da organização
(AJUDANTES.md, ERROS_VALIDADOR.md, MANUTENCAO.md e este script), os ocultos e os caches.

Quem usa:
  - o build da imagem web do Boca-Game-Jam-Pet (Dockerfile, estágio dist);
  - a skill boca-desafio (desafio.py --starter e --conferir importam este módulo).

Uso:
    python3 empacotar_kit.py --saida starter_kit.zip [--pasta DIR]
Só a biblioteca padrão. Código 1 se faltar algum arquivo obrigatório.
"""

import argparse
import os
import sys
import zipfile

PASTA_RAIZ_ZIP = "starter_kit"
DATA_FIXA = (2026, 1, 1, 0, 0, 0)  # datas fixas: o mesmo kit gera o mesmo zip
EXCLUIDOS = {"AJUDANTES.md", "ERROS_VALIDADOR.md", "MANUTENCAO.md", "empacotar_kit.py"}
OBRIGATORIOS = [
    "README.md",
    "c/bot.c", "c/arena.h",
    "cpp/bot.cpp", "cpp/nlohmann/json.hpp",
    "java/MeuBot.java", "java/gson.jar",
    "python/bot.py",
]


def ignorado(nome):
    """Nomes que nunca entram no zip: ocultos, caches Python e os arquivos internos."""
    return (nome.startswith(".") or nome == "__pycache__" or nome in EXCLUIDOS
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
    gravar_zip(saida, arquivos)
    return 0, f"OK zip: {len(arquivos)} arquivos -> {saida}"


def main():
    ap = argparse.ArgumentParser(description="Gera o starter_kit.zip das equipes.")
    ap.add_argument("--saida", required=True, help="caminho do zip a gerar")
    ap.add_argument("--pasta", default=os.path.dirname(os.path.abspath(__file__)),
                    help="pasta do kit (padrão: a deste script)")
    args = ap.parse_args()
    codigo, msg = empacotar(args.pasta, args.saida)
    print(msg)
    return codigo


if __name__ == "__main__":
    sys.exit(main())
