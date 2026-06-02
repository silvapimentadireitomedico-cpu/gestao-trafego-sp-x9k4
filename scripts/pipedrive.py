"""Módulo Pipedrive — conta leads novos + ganhos (won_time) por funil em um período."""
import json
import os
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

BRT = timezone(timedelta(hours=-3))
DOMAIN = "silvapimenta"

# pipeline_id → slug usado no dashboard
FUNIS = {
    1: "aux-moradia",
    2: "fies",
    3: "_seguro_geral",   # split em seguro (não-vida) e seg-vida via custom field
    4: "fies-suspensao",
    6: "direito-medico",
    8: "inss",
    9: "provab",
    10: "livre-ir",
}


def _token() -> str:
    t = os.environ.get("PIPEDRIVE_TOKEN")
    if not t:
        raise RuntimeError("PIPEDRIVE_TOKEN não está no ambiente")
    return t


def _http_get(url: str) -> dict:
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def _base_v1() -> str:
    return f"https://{DOMAIN}.pipedrive.com/api/v1"


def _base_v2() -> str:
    return f"https://{DOMAIN}.pipedrive.com/api/v2"


def _campo_tipo_seguro() -> str | None:
    url = f"{_base_v1()}/dealFields?api_token={_token()}&limit=500"
    data = _http_get(url).get("data") or []
    for f in data:
        nome = (f.get("name") or "").strip().lower()
        if "tipo" in nome and "seguro" in nome:
            return f.get("key")
    return None


def _tipo_seguro_do_deal(deal: dict, key: str) -> str:
    if not key:
        return ""
    valor = None
    cf = deal.get("custom_fields") or {}
    if key in cf and cf[key] not in (None, ""):
        valor = cf[key]
    if valor in (None, ""):
        valor = deal.get(key)
    if not valor:
        return ""
    return str(valor).strip().lower()


def _contar_funil(pipeline_id: int, inicio: datetime, fim: datetime, campo_seguro: str | None):
    total = {
        "geral": {"leads_novos": 0, "ganhos": 0, "valor_ganhos": 0.0},
        "vida": {"leads_novos": 0, "ganhos": 0, "valor_ganhos": 0.0},
        "nao_vida": {"leads_novos": 0, "ganhos": 0, "valor_ganhos": 0.0},
    }
    cursor = None
    while True:
        params = {"api_token": _token(), "pipeline_id": pipeline_id, "limit": 500}
        if cursor:
            params["cursor"] = cursor
        url = f"{_base_v2()}/deals?{urllib.parse.urlencode(params)}"
        body = _http_get(url)
        for d in body.get("data") or []:
            add_time = d.get("add_time")
            won_time = d.get("won_time")
            status = d.get("status")
            valor = float(d.get("value") or 0)
            ehvida = pipeline_id == 3 and _tipo_seguro_do_deal(d, campo_seguro) == "vida"
            bucket = "vida" if ehvida else "nao_vida"
            if add_time:
                add_dt = datetime.fromisoformat(add_time.replace("Z", "+00:00"))
                if inicio <= add_dt <= fim:
                    total["geral"]["leads_novos"] += 1
                    if pipeline_id == 3:
                        total[bucket]["leads_novos"] += 1
            if status == "won" and won_time:
                won_dt = datetime.fromisoformat(won_time.replace("Z", "+00:00"))
                if inicio <= won_dt <= fim:
                    total["geral"]["ganhos"] += 1
                    total["geral"]["valor_ganhos"] += valor
                    if pipeline_id == 3:
                        total[bucket]["ganhos"] += 1
                        total[bucket]["valor_ganhos"] += valor
        cursor = (body.get("additional_data") or {}).get("next_cursor")
        if not cursor:
            break
    return total


def coletar(inicio_iso: str, fim_iso: str) -> dict:
    """Retorna dict produto_slug → {leads_novos, ganhos, valor_ganhos}.
    Datas em Brasília (UTC-3) pra bater com Insights do Pipedrive.
    """
    inicio = datetime.fromisoformat(inicio_iso + "T00:00:00-03:00")
    fim = datetime.fromisoformat(fim_iso + "T23:59:59-03:00")
    campo_seguro = _campo_tipo_seguro()

    saida = {}
    for pid, slug in FUNIS.items():
        r = _contar_funil(pid, inicio, fim, campo_seguro)
        if pid == 3:
            saida["seguro"] = r["nao_vida"]
            saida["seg-vida"] = r["vida"]
        else:
            saida[slug] = r["geral"]
    return saida


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Uso: python pipedrive.py YYYY-MM-DD YYYY-MM-DD")
        sys.exit(1)
    print(json.dumps(coletar(sys.argv[1], sys.argv[2]), indent=2, ensure_ascii=False))
