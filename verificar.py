#!/usr/bin/env python3
"""
Verificador do bot - Game Jam PET 2026
=====================================
Confere o seu bot ANTES de enviar, do mesmo jeito que o BOCA e a arena fazem:

  1. Validação: as mesmas regras do validador do BOCA (main, assinatura do pensar,
     package, bibliotecas...). Com erro aqui, o BOCA responderia Compilation Error.
  2. Montagem: compila o bot junto com o código da arena (wrappers), como na partida.
     Pega main() repetida, assinatura errada e erros de ligação.
  3. Teste rodando: executa o seu pensar() em centenas de estados de jogo e confere
     o tempo de cada resposta (limite de 50 ms por tick), os campos da ação e os erros.

Uso (na pasta do kit):
    python3 verificar.py python/bot.py
    python3 verificar.py c/bot.c --ticks 600
    python3 verificar.py treino/01_andar/bot.py --treino   (estados com os pontos do objetivo)

Precisa do Python 3.10+. As etapas 2 e 3 precisam do compilador da sua linguagem
(gcc, g++ ou javac) e do bash: no Windows, rode no WSL. Em Python, a etapa 3 também
roda no Windows sem o bash.

O teste rodando NÃO é uma partida: os adversários andam em círculos e não atiram.
Ele serve para achar erros e lentidão, não para medir a força da estratégia.
"""

import argparse
import base64
import json
import math
import os
import queue
import random
import shutil
import subprocess
import sys
import tempfile
import threading
import time

KIT = os.path.dirname(os.path.abspath(__file__))
VERIFICADOR = os.path.join(KIT, "verificador")
# Arquivos de apoio de cada linguagem (pasta do kit, nome): cópias dos do servidor
APOIO = [("c", "arena.h"), ("cpp", "arena.hpp"), ("java", "Arena.java"), ("python", "arena.py")]

LINGUAGENS = {".c": "c", ".cpp": "cpp", ".java": "java", ".py": "py"}
NOME_LINGUAGEM = {"c": "C", "cpp": "C++", "java": "Java", "py": "Python 3"}

# Limites da arena (iguais aos da engine)
PRAZO_MS = 50            # resposta de cada tick
PRAZO_TICK0_MS = 5000    # o tick 0 dá tempo para o programa iniciar (a JVM é lenta)
FOLGA_MS = 35            # acima disto já é arriscado: o servidor roda até 20 bots
ESPERA_MAX_S = 3.0       # sem resposta depois disto, o teste desiste
OPCOES_JAVA = ["-Xmx512m", "-XX:CompressedClassSpaceSize=64m", "-XX:+UseSerialGC"]
CAMPOS = {"throttle": "numero", "turn": "numero", "turret_angle": "numero", "shoot": "bool", "shield": "bool"}

# Cores só em terminal de verdade
COR = sys.stdout.isatty() and os.environ.get("NO_COLOR") is None


def cor(texto, codigo):
    return f"\033[{codigo}m{texto}\033[0m" if COR else texto


class Relatorio:
    def __init__(self):
        self.erros = 0
        self.avisos = 0

    def etapa(self, titulo):
        print("\n" + cor(titulo, "1"))

    def ok(self, msg):
        print(f"  {cor('[OK]', '32')}    {msg}")

    def aviso(self, msg, dica=""):
        self.avisos += 1
        print(f"  {cor('[AVISO]', '33')} {msg}")
        if dica:
            print(f"          dica: {dica}")

    def erro(self, msg, dica=""):
        self.erros += 1
        print(f"  {cor('[ERRO]', '31')}  {msg}")
        if dica:
            print(f"          dica: {dica}")

    def info(self, msg):
        print(f"          {msg}")


# ------------------------------------------------------------------------------
# Etapa 1: validação (os mesmos scripts do validador do BOCA)
# ------------------------------------------------------------------------------
def validar(lang, arquivo, rel):
    rel.etapa("1. Validação (as mesmas regras do validador do BOCA)")
    if lang == "py":
        cmd = [sys.executable, "-I", os.path.join(VERIFICADOR, "checar_python.py"), arquivo]
    else:
        cmd = [sys.executable, "-I", os.path.join(VERIFICADOR, "checar_fonte.py"), lang, arquivo]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode == 0:
        rel.ok("o validador do BOCA aceitaria este arquivo")
        return True
    msg = (r.stderr or r.stdout).strip() or f"o validador saiu com código {r.returncode}"
    for linha in msg.splitlines()[:6]:
        rel.erro(linha)
    rel.info("o BOCA responderia Compilation Error, com esta mesma mensagem no [Ver Erro]")
    return False


# ------------------------------------------------------------------------------
# Etapa 2: montagem igual à da arena (build_bot.sh + wrappers)
# ------------------------------------------------------------------------------
def montar_raiz(tmp):
    """Monta o layout que o build_bot.sh espera: wrappers/, engine/nlohmann/, libs/."""
    raiz = os.path.join(tmp, "arena")
    wrappers = os.path.join(raiz, "wrappers")
    os.makedirs(wrappers)
    for nome in os.listdir(VERIFICADOR):
        shutil.copy2(os.path.join(VERIFICADOR, nome), os.path.join(wrappers, nome))
    # Arquivos de apoio (o que o "#include"/"import" da equipe usa): os mesmos do servidor
    for pasta, nome in APOIO:
        shutil.copy2(os.path.join(KIT, pasta, nome), os.path.join(wrappers, nome))
    os.makedirs(os.path.join(raiz, "engine", "nlohmann"))
    shutil.copy2(os.path.join(KIT, "cpp", "nlohmann", "json.hpp"), os.path.join(raiz, "engine", "nlohmann", "json.hpp"))
    os.makedirs(os.path.join(raiz, "libs"))
    shutil.copy2(os.path.join(KIT, "java", "gson.jar"), os.path.join(raiz, "libs", "gson-2.10.1.jar"))
    return raiz


def montar_python_sem_bash(arquivo, exe):
    """O mesmo executável que o build_bot.sh gera para Python (código embutido + wrapper)."""
    with open(arquivo, "rb") as f:
        fonte = base64.b64encode(f.read()).decode("ascii")
    with open(os.path.join(VERIFICADOR, "wrapper.py"), encoding="utf-8") as f:
        wrapper = f.read()
    with open(os.path.join(KIT, "python", "arena.py"), "rb") as f:
        apoio = base64.b64encode(f.read()).decode("ascii")
    with open(exe, "w", encoding="utf-8", newline="\n") as f:
        f.write(f'#!/usr/bin/env python3\n_FONTE_DA_EQUIPE = "{fonte}"\n_FONTE_ARENA = "{apoio}"\n{wrapper}')


def falta_ferramenta(lang):
    precisa = {"c": ["bash", "gcc", "g++"], "cpp": ["bash", "g++"], "java": ["bash", "javac", "jar", "java"],
               "py": ["bash"]}[lang]
    return [p for p in precisa if shutil.which(p) is None]


def montar(lang, arquivo, tmp, rel):
    rel.etapa("2. Montagem (o seu código junto com o código da arena, como na partida)")
    exe = os.path.join(tmp, "bot.jar" if lang == "java" else "bot.exe")
    faltam = falta_ferramenta(lang)
    if faltam and lang == "py":
        montar_python_sem_bash(arquivo, exe)
        rel.ok("montado (sem bash: o verificador montou o Python do mesmo jeito que a arena)")
        return exe
    if faltam:
        rel.aviso(f"etapa pulada: falta {', '.join(faltam)} nesta máquina",
                  "no Linux, instale o compilador (ex.: sudo apt install build-essential default-jdk); "
                  "no Windows, rode este verificador no WSL")
        return None
    raiz = montar_raiz(tmp)
    env = dict(os.environ, TOPCOM_WRAPPERS_BUILD=os.path.join(tmp, "cache"), LC_ALL="C")
    r = subprocess.run(["bash", os.path.join(raiz, "wrappers", "build_bot.sh"), arquivo, exe],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
    if r.returncode != 0 or not os.path.exists(exe):
        saida = (r.stderr + "\n" + r.stdout).strip().splitlines()
        rel.erro("a montagem falhou: o BOCA responderia Compilation Error")
        for linha in saida[:15]:
            rel.info(linha.replace(raiz, "<arena>"))
        return None
    rel.ok("compilou junto com o código da arena")
    return exe


# ------------------------------------------------------------------------------
# Etapa 3: teste rodando
# ------------------------------------------------------------------------------
def comando_execucao(lang, exe):
    if lang == "py":
        return [sys.executable, exe]
    if lang == "java":
        return ["java"] + OPCOES_JAVA + ["-jar", exe]
    return [exe]


class Mundo:
    """Gera estados no formato da arena. O seu tanque se move de acordo com a ação que você
    devolve; os adversários andam em círculos; perigos e itens aparecem e somem."""

    def __init__(self, seed, treino=False):
        self.rng = random.Random(seed)
        # --treino: pontos do objetivo, como nas fases da guia Treino
        self.pontos = [{"id": f"P{i + 1}", "x": round(self.rng.uniform(100, 900), 3),
                        "y": round(self.rng.uniform(100, 900), 3), "raio": 30.0} for i in range(4)] if treino else None
        self.eu = {"id": 1, "x": 500.0, "y": 140.0, "vx": 0.0, "vy": 0.0, "angle": 90.0, "turret_angle": 90.0,
                   "hp": 100.0, "energy": 100.0, "cooldown": 0.0, "shield": False}
        self.inimigos = [self._inimigo(i + 2) for i in range(5)]

    def _inimigo(self, ident):
        return {"id": ident, "cx": self.rng.uniform(150, 850), "cy": self.rng.uniform(150, 850),
                "r": self.rng.uniform(40, 200), "fase": self.rng.uniform(0, 2 * math.pi),
                "w": self.rng.choice([-1, 1]) * self.rng.uniform(0.02, 0.08)}

    def _quantos_inimigos(self, tick, total):
        # Casos extremos de propósito: arena cheia (19 adversários) e nenhum adversário
        if total - 40 <= tick < total - 20:
            return 19
        if total - 20 <= tick < total - 10:
            return 0
        return 5

    def estado(self, tick, total):
        n = self._quantos_inimigos(tick, total)
        while len(self.inimigos) < n:
            self.inimigos.append(self._inimigo(len(self.inimigos) + 2))
        inimigos = []
        for k, it in enumerate(self.inimigos[:n]):
            a = it["fase"] + it["w"] * tick
            x, y = it["cx"] + it["r"] * math.cos(a), it["cy"] + it["r"] * math.sin(a)
            v = it["w"] * it["r"] * 10
            inimigos.append({"id": it["id"], "x": round(x, 3), "y": round(y, 3),
                             "vx": round(-math.sin(a) * v, 3), "vy": round(math.cos(a) * v, 3)})
        perigos = []
        if tick % 60 >= 20:
            perigos.append({"type": "ARTILLERY", "x": 300.0, "y": 600.0, "radius": 104.0 if tick > 400 else 80.0,
                            "timer": round(max(0.0, 3.0 - (tick % 60 - 20) * 0.1), 2), "angle": 0.0,
                            "duration": 0.0, "id": 1000 + tick // 60})
        if tick % 150 >= 100:
            perigos.append({"type": "LASER", "x": 500.0, "y": 500.0, "radius": 0.0, "timer": 0.0,
                            "angle": (tick * 3.0) % 360.0, "duration": 5.0, "id": 2000 + tick // 150})
        if total - 30 <= tick < total - 25:
            perigos += [{"type": "ARTILLERY", "x": 100.0 + 180 * i, "y": 900.0, "radius": 104.0, "timer": 1.5,
                         "angle": 0.0, "duration": 0.0, "id": 3000 + i} for i in range(3)]
        itens = [{"id": 5000 + i, "type": "HEAL" if i % 2 else "ENERGY", "x": 200.0 + 200 * i, "y": 820.0}
                 for i in range(4 if tick % 100 < 50 else 1)]
        self.eu["shield"] = bool(self.eu["shield"])
        estado = {"enemies": inimigos, "hazards": perigos, "items": itens,
                  "self": {k: (round(v, 3) if isinstance(v, float) else v) for k, v in self.eu.items()},
                  "tick": tick}
        if self.pontos is not None:
            estado["objetivo"] = {"pontos": self.pontos}
        return estado

    def aplicar(self, acao):
        """Aplica a ação ao seu tanque (cinemática da arena, simplificada)."""
        def numero(campo, padrao):
            v = acao.get(campo, padrao)
            return float(v) if isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v) else padrao
        throttle = max(-1.0, min(1.0, numero("throttle", 0.0)))
        turn = max(-1.0, min(1.0, numero("turn", 0.0)))
        eu = self.eu
        eu["angle"] = (eu["angle"] + turn * 9.0) % 360.0
        eu["turret_angle"] = numero("turret_angle", eu["turret_angle"]) % 360.0
        rad = math.radians(eu["angle"])
        eu["vx"], eu["vy"] = math.cos(rad) * throttle * 50.0, math.sin(rad) * throttle * 50.0
        eu["x"] = max(20.0, min(980.0, eu["x"] + eu["vx"] * 0.1))
        eu["y"] = max(20.0, min(980.0, eu["y"] + eu["vy"] * 0.1))
        eu["cooldown"] = max(0.0, eu["cooldown"] - 0.1)
        if acao.get("shoot") in (True, 1) and eu["cooldown"] <= 0 and eu["energy"] >= 20:
            eu["cooldown"], eu["energy"] = 1.0, eu["energy"] - 20
        quer_escudo = acao.get("shield") in (True, 1)
        if quer_escudo and (eu["shield"] or eu["energy"] > 50):
            eu["energy"] -= 5.0
            eu["shield"] = eu["energy"] > 0
        else:
            eu["shield"] = False
        eu["energy"] = max(0.0, min(100.0, eu["energy"] + 0.5))


def _ler_saida(stream, fila):
    for linha in iter(stream.readline, ""):
        fila.put((time.perf_counter(), linha))
    fila.put((time.perf_counter(), None))


def _ler_erro(stream, linhas):
    for linha in iter(stream.readline, ""):
        linhas.append(linha.rstrip("\n"))


def _sem_nan(valor):
    raise ValueError(valor)


def conferir_acao(texto, problemas):
    """Confere uma resposta. Devolve o dict da ação (ou {} se for inválida)."""
    try:
        acao = json.loads(texto, parse_constant=_sem_nan)
    except ValueError:
        problemas["nao_json"] += 1
        return {}
    if not isinstance(acao, dict):
        problemas["nao_objeto"] += 1
        return {}
    if not acao:
        problemas["vazia"] += 1
    for campo, valor in acao.items():
        tipo = CAMPOS.get(campo)
        if tipo is None:
            problemas["desconhecido"].add(campo)
        elif valor is None:
            problemas["nulo"].add(campo)
        elif tipo == "numero":
            if isinstance(valor, bool) or not isinstance(valor, (int, float)):
                problemas["tipo"].add(f"{campo} = {json.dumps(valor)} (devia ser número)")
            elif campo in ("throttle", "turn") and abs(valor) > 1.0:
                problemas["fora"].add(campo)
        elif tipo == "bool" and not isinstance(valor, bool):
            if isinstance(valor, (int, float)):
                problemas["bool_numero"].add(campo)
            else:
                problemas["tipo"].add(f"{campo} = {json.dumps(valor)} (devia ser true/false)")
    return acao


def testar(lang, exe, ticks, seed, rel, treino=False):
    rel.etapa(f"3. Teste rodando ({ticks} ticks de jogo, um estado por tick)")
    cmd = comando_execucao(lang, exe)
    try:
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True, encoding="utf-8", errors="replace", bufsize=1)
    except OSError as e:
        rel.erro(f"não foi possível executar o bot: {e}")
        return
    fila, stderr = queue.Queue(), []
    threading.Thread(target=_ler_saida, args=(proc.stdout, fila), daemon=True).start()
    threading.Thread(target=_ler_erro, args=(proc.stderr, stderr), daemon=True).start()

    mundo = Mundo(seed, treino)
    problemas = {"nao_json": 0, "nao_objeto": 0, "vazia": 0, "desconhecido": set(), "nulo": set(),
                 "tipo": set(), "fora": set(), "bool_numero": set()}
    tempos, lentos, tick0_ms, extras, morreu = [], [], None, 0, None
    respondidos = 0
    for tick in range(ticks):
        estado = mundo.estado(tick, ticks)
        try:
            proc.stdin.write(json.dumps(estado, separators=(",", ":")) + "\n")
            proc.stdin.flush()
        except (BrokenPipeError, OSError):
            morreu = tick
            break
        inicio = time.perf_counter()
        try:
            chegada, linha = fila.get(timeout=ESPERA_MAX_S if tick else max(ESPERA_MAX_S, PRAZO_TICK0_MS / 1000 + 5))
        except queue.Empty:
            rel.erro(f"o bot não respondeu ao tick {tick} em {ESPERA_MAX_S:.0f} s: na arena ele seria eliminado",
                     "procure laços sem fim ou leitura do teclado (input/scanf/cin) no seu código")
            break
        if linha is None:
            morreu = tick
            break
        ms = (chegada - inicio) * 1000
        if tick == 0:
            tick0_ms = ms
        else:
            tempos.append(ms)
            if ms > PRAZO_MS:
                lentos.append((tick, ms))
        respondidos += 1
        mundo.aplicar(conferir_acao(linha.strip(), problemas))
        # Mais de uma linha para um só estado: algo escreve na saída da arena
        while not fila.empty():
            _, sobra = fila.get_nowait()
            if sobra is None:
                morreu = tick
                break
            extras += 1

    try:
        proc.stdin.close()
    except OSError:
        pass
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()
    time.sleep(0.1)

    # --- relatório do teste ---
    if morreu is not None:
        rel.erro(f"o programa do bot terminou no tick {morreu}: na arena ele seria desconectado e eliminado",
                 "veja as mensagens de erro abaixo (crash, exit(), exceção fora do pensar)")
    elif respondidos == ticks:
        rel.ok(f"respondeu aos {ticks} estados, uma resposta por tick")

    if tick0_ms is not None:
        if tick0_ms > PRAZO_TICK0_MS:
            rel.erro(f"tick 0 levou {tick0_ms:.0f} ms (limite {PRAZO_TICK0_MS} ms para iniciar)")
        else:
            rel.ok(f"início (tick 0): {tick0_ms:.0f} ms (limite {PRAZO_TICK0_MS} ms)")
    if tempos:
        ordenados = sorted(tempos)
        p95 = ordenados[min(len(ordenados) - 1, int(len(ordenados) * 0.95))]
        resumo = f"tempo por tick: médio {sum(tempos) / len(tempos):.2f} ms, p95 {p95:.2f} ms, máximo {max(tempos):.2f} ms"
        if lentos:
            rel.erro(f"{len(lentos)} tick(s) acima de {PRAZO_MS} ms ({resumo})",
                     "na arena cada um desses ticks é perdido, e 20 seguidos eliminam o bot. "
                     "Corte buscas pesadas, evite recriar estruturas grandes a cada tick e limite laços")
            for t, ms in lentos[:5]:
                rel.info(f"tick {t}: {ms:.1f} ms")
        elif p95 > FOLGA_MS:
            rel.aviso(f"{resumo}: perto do limite de {PRAZO_MS} ms",
                      "o servidor pode ser mais lento que esta máquina; deixe folga")
        else:
            rel.ok(resumo + f" (limite {PRAZO_MS} ms)")

    falhas_pensar = sum(1 for l in stderr if l.startswith("[ERRO NO BOT"))
    if falhas_pensar:
        rel.erro(f"o pensar() falhou em {falhas_pensar} tick(s): neles a arena usa a ação parada ({{}})",
                 "corrija a exceção mostrada abaixo; o tanque fica parado nesses ticks")
    if problemas["nao_json"] or problemas["nao_objeto"]:
        rel.erro(f"{problemas['nao_json'] + problemas['nao_objeto']} resposta(s) não são um objeto JSON "
                 "(valem como ação parada)")
    if problemas["tipo"]:
        rel.erro("campos com tipo errado (a arena ignora o campo e usa o padrão): " + ", ".join(sorted(problemas["tipo"])))
    if problemas["nulo"]:
        rel.erro("campos com valor nulo/NaN (a arena ignora o campo): " + ", ".join(sorted(problemas["nulo"])),
                 "algum cálculo deu NaN (ex.: divisão por zero, raiz de negativo, acos fora de [-1, 1])")
    if problemas["bool_numero"]:
        rel.aviso("shoot/shield como número (" + ", ".join(sorted(problemas["bool_numero"])) +
                  "): a arena aceita (diferente de 0 = sim), mas use true/false")
    if problemas["fora"]:
        rel.aviso("valores fora de [-1, 1] em " + ", ".join(sorted(problemas["fora"])) + ": a arena corta para o limite")
    if problemas["desconhecido"]:
        rel.aviso("campos que a arena não conhece (ignorados): " + ", ".join(sorted(problemas["desconhecido"])),
                  "os campos da ação são throttle, turn, turret_angle, shoot e shield")
    if problemas["vazia"] and not falhas_pensar:
        rel.aviso(f"{problemas['vazia']} resposta(s) vazias ({{}}): o tanque fica parado nesses ticks")
    if extras:
        rel.erro(f"{extras} linha(s) a mais na saída da arena",
                 "algo escreve direto na saída padrão (fora do pensar ou por um caminho que o wrapper não protege)")

    mensagens = [l for l in stderr if l.strip()]
    if mensagens:
        rel.info("")
        rel.info(f"saída de erro do bot (stderr: prints e erros; {len(mensagens)} linha(s), primeiras abaixo):")
        for l in mensagens[:12]:
            rel.info("  | " + l[:160])


def main():
    ap = argparse.ArgumentParser(description="Confere o bot antes de enviar (validação, montagem e teste rodando).")
    ap.add_argument("arquivo", help="o arquivo do bot: .c, .cpp, .java ou .py")
    ap.add_argument("--ticks", type=int, default=300, help="ticks do teste rodando (padrão 300)")
    ap.add_argument("--seed", type=int, default=2026, help="semente dos estados gerados (padrão 2026)")
    ap.add_argument("--treino", action="store_true", help="estados com objetivo (pontos), como na guia Treino")
    args = ap.parse_args()

    if sys.version_info < (3, 10):
        print("Este verificador precisa do Python 3.10 ou mais novo.")
        return 2
    arquivo = os.path.abspath(args.arquivo)
    lang = LINGUAGENS.get(os.path.splitext(arquivo)[1].lower())
    if not os.path.isfile(arquivo):
        print(f"Arquivo não encontrado: {args.arquivo}")
        return 2
    if lang is None:
        print("Extensão não suportada: use .c, .cpp, .java ou .py")
        return 2

    print(cor(f"Verificador do bot - {os.path.basename(arquivo)} ({NOME_LINGUAGEM[lang]})", "1"))
    rel = Relatorio()
    tmp = tempfile.mkdtemp(prefix="verificar_bot_")
    try:
        if validar(lang, arquivo, rel):
            exe = montar(lang, arquivo, tmp, rel)
            if exe:
                testar(lang, exe, max(30, args.ticks), args.seed, rel, args.treino)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print()
    if rel.erros:
        print(cor(f"RESULTADO: {rel.erros} erro(s) e {rel.avisos} aviso(s). Corrija os erros antes de enviar.", "31"))
        return 1
    if rel.avisos:
        print(cor(f"RESULTADO: sem erros, {rel.avisos} aviso(s).", "33"))
        return 0
    print(cor("RESULTADO: tudo certo. Envie pela guia " + ("Treino" if args.treino else "Runs") + " do BOCA.", "32"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
