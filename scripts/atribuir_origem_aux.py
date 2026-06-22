"""Cruzamento lead-a-lead de ORIGEM (Auxílio Moradia) — instrução William 22/06.

A automação Tag Lead grava em cada PESSOA do Pipedrive: NÚMERO DA CAMPANHA, PUBLICO,
CRIATIVO. Este script pega os deals do funil Aux Moradia (pipeline 1) no período,
lê a origem na pessoa de cada um, e TABULA a origem real, com foco em quem traz LIXO /
AÇÃO INVIÁVEL (sem inferência: só com a origem verificada lead a lead).

Roda como enriquecimento: mescla o resultado em data/rita/aux-moradia.json sob
pipedrive.atribuicao_origem. Depois o gerar_relatorio_rita.py usa esse dado pra cravar
a origem com número e nome (Passo 2b do playbook).

Uso: python scripts/atribuir_origem_aux.py   (PIPEDRIVE_TOKEN no ambiente)
"""
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pipedrive

ROOT = Path(__file__).resolve().parent.parent
AUX_JSON = ROOT / "data" / "rita" / "aux-moradia.json"
BRT = timezone(timedelta(hours=-3))
PIPELINE_AUX = 1
JANELAS = [30, 14, 7]

# Campos custom da PESSOA gravados pelo Tag Lead (keys confirmadas via personFields)
F_CAMPANHA = "4b3b309495d5824b2324298d7314d500dda69f61"
F_PUBLICO = "cd26c142a44d92ac9a88656c5cd4c06824279ab4"
F_CRIATIVO = "3bc1cc8528fb29f77b573ee5371906ccb7197eb7"
MOTIVOS_LIXO = {"LIXO", "AÇÃO INVIÁVEL", "ACAO INVIAVEL", "INVIÁVEL", "INVIAVEL"}


def _person_id(deal) -> int | None:
    p = deal.get("person_id")
    if isinstance(p, dict):
        p = p.get("value") or p.get("id")
    try:
        return int(p)
    except (TypeError, ValueError):
        return None


def _origem_pessoa(pid: int, cache: dict) -> dict:
    if pid in cache:
        return cache[pid]
    tok = pipedrive._token()
    url = f"{pipedrive._base_v1()}/persons/{pid}?api_token={tok}"
    o = {"campanha": "", "publico": "", "criativo": ""}
    for tent in range(4):
        try:
            d = pipedrive._http_get(url).get("data") or {}
            o = {
                "campanha": (d.get(F_CAMPANHA) or "").strip(),
                "publico": (d.get(F_PUBLICO) or "").strip(),
                "criativo": (d.get(F_CRIATIVO) or "").strip(),
            }
            break
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(2 * (tent + 1))
                continue
            break
        except Exception:
            break
    cache[pid] = o
    return o


def coletar():
    hoje = datetime.now(BRT).date()
    janelas = {f"{n}d": (datetime.combine(hoje - timedelta(days=n), datetime.min.time(), BRT),
                         datetime.combine(hoje - timedelta(days=1), datetime.max.time(), BRT))
               for n in JANELAS}
    inicio_max = janelas[f"{max(JANELAS)}d"][0]
    fim = janelas[f"{max(JANELAS)}d"][1]

    print("Puxando deals do funil Aux Moradia (pipeline 1)...")
    deals = []
    cursor = None
    while True:
        params = {"api_token": pipedrive._token(), "pipeline_id": PIPELINE_AUX, "limit": 500}
        if cursor:
            params["cursor"] = cursor
        body = pipedrive._http_get(f"{pipedrive._base_v2()}/deals?{urllib.parse.urlencode(params)}")
        deals.extend(body.get("data") or [])
        cursor = (body.get("additional_data") or {}).get("next_cursor")
        if not cursor:
            break

    # deals da janela de 30d por add_time
    no_periodo = []
    for d in deals:
        at = d.get("add_time")
        if not at:
            continue
        adt = datetime.fromisoformat(at.replace("Z", "+00:00"))
        if inicio_max <= adt <= fim:
            no_periodo.append((d, adt))
    print(f"  {len(no_periodo)} leads no periodo de 30d; lendo origem na pessoa de cada um...")

    cache = {}
    registros = []  # cada lead com origem + status + motivo + janela
    for i, (d, adt) in enumerate(no_periodo):
        pid = _person_id(d)
        org = _origem_pessoa(pid, cache) if pid else {"campanha": "", "publico": "", "criativo": ""}
        motivo = (d.get("lost_reason") or "").strip()
        registros.append({
            "add_dt": adt,
            "status": d.get("status"),
            "motivo": motivo,
            "campanha": org["campanha"] or "(sem)",
            "publico": org["publico"] or "(sem)",
            "criativo": org["criativo"] or "(sem)",
        })
        if (i + 1) % 50 == 0:
            print(f"    {i+1}/{len(no_periodo)}")
        time.sleep(0.08)  # throttle leve

    # Tabula por janela
    saida = {"keys": {"campanha": F_CAMPANHA, "publico": F_PUBLICO, "criativo": F_CRIATIVO},
             "obtido_em": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
             "janelas": {}}
    for jan, (ini, _f) in janelas.items():
        regs = [r for r in registros if r["add_dt"] >= ini]
        por_origem = {}  # (campanha,publico,criativo) -> contadores
        cobertura = {"com_origem": 0, "sem_origem": 0}
        for r in regs:
            chave = f"{r['campanha']} | {r['publico']} | {r['criativo']}"
            if r["campanha"] == "(sem)" and r["publico"] == "(sem)" and r["criativo"] == "(sem)":
                cobertura["sem_origem"] += 1
            else:
                cobertura["com_origem"] += 1
            o = por_origem.setdefault(chave, {"campanha": r["campanha"], "publico": r["publico"],
                                              "criativo": r["criativo"], "total": 0, "won": 0,
                                              "lost": 0, "open": 0, "lixo": 0, "por_motivo": {}})
            o["total"] += 1
            if r["status"] == "won":
                o["won"] += 1
            elif r["status"] == "lost":
                o["lost"] += 1
                m = r["motivo"] or "(sem motivo)"
                o["por_motivo"][m] = o["por_motivo"].get(m, 0) + 1
                if (r["motivo"] or "").upper() in MOTIVOS_LIXO:
                    o["lixo"] += 1
            else:
                o["open"] += 1
        ordenado = sorted(por_origem.values(), key=lambda x: (x["lixo"], x["total"]), reverse=True)
        saida["janelas"][jan] = {
            "total_leads": len(regs),
            "cobertura_origem": cobertura,
            "por_origem": ordenado,
        }
    return saida


def main():
    if not os.environ.get("PIPEDRIVE_TOKEN"):
        print("ERRO: PIPEDRIVE_TOKEN ausente no ambiente.")
        return 2
    atrib = coletar()
    if not AUX_JSON.exists():
        print(f"ERRO: {AUX_JSON} nao existe; rode o rita_collector aux-moradia antes.")
        return 3
    data = json.loads(AUX_JSON.read_text(encoding="utf-8"))
    data.setdefault("pipedrive", {})["atribuicao_origem"] = atrib
    AUX_JSON.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    j30 = atrib["janelas"]["30d"]
    print(f"\nOK -> mesclado em {AUX_JSON.name}")
    print(f"30d: {j30['total_leads']} leads, cobertura origem {j30['cobertura_origem']}")
    print("Top origens por LIXO (30d):")
    for o in j30["por_origem"][:6]:
        print(f"  [{o['lixo']} lixo / {o['total']} leads · won {o['won']}] {o['campanha']} | {o['publico']} | {o['criativo']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
