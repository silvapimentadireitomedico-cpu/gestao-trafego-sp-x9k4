"""Coletor principal — chama Google Ads + Meta Ads + Pipedrive + PTAX e gera data.json.

Uso (modo padrão = mês corrente):
    python scripts/coletar.py

Uso (mês específico):
    python scripts/coletar.py --mes 2026-05

Gera (relativo à raiz do repo):
    data/data.json                          (mês corrente)
    data/data-fechamento-YYYY-MM.json       (mês fechado, se --mes foi passado e não é o atual)
"""
import argparse
import json
import os
import sys
from calendar import monthrange
from datetime import date, datetime
from pathlib import Path

# import dos módulos vizinhos
sys.path.insert(0, str(Path(__file__).resolve().parent))
import google_ads
import meta_ads
import pipedrive
import ptax


ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"


def _arg_mes() -> tuple[str, int, int, date, date, bool]:
    """Retorna (mes_referencia, ano, mes, dt_inicio, dt_fim, eh_corrente)."""
    p = argparse.ArgumentParser()
    p.add_argument("--mes", help="YYYY-MM (default = mês atual)")
    args = p.parse_args()
    hoje = date.today()
    if args.mes:
        ano, mes = (int(x) for x in args.mes.split("-"))
    else:
        ano, mes = hoje.year, hoje.month
    inicio = date(ano, mes, 1)
    fim_dia = monthrange(ano, mes)[1]
    fim = date(ano, mes, fim_dia)
    mes_ref = f"{ano}-{mes:02d}"
    eh_corrente = (ano, mes) == (hoje.year, hoje.month)
    return mes_ref, ano, mes, inicio, fim, eh_corrente


def main():
    mes_ref, ano, mes, dt_inicio, dt_fim, eh_corrente = _arg_mes()
    print(f"== Coletando {mes_ref} ({dt_inicio} → {dt_fim}, corrente={eh_corrente}) ==")

    # 1. PTAX
    taxa_usd, fonte_usd = ptax.cotacao()
    print(f"PTAX: {taxa_usd:.4f} ({fonte_usd})")

    # 2. Google Ads
    print("Google Ads...")
    try:
        gads = google_ads.coletar(since=dt_inicio.isoformat(), until=dt_fim.isoformat())
    except Exception as e:
        print(f"  ERRO Google Ads: {e}")
        gads = {}

    # 3. Meta Ads
    print("Meta Ads...")
    try:
        meta = meta_ads.coletar(dt_inicio.isoformat(), dt_fim.isoformat(), taxa_usd)
    except Exception as e:
        print(f"  ERRO Meta Ads: {e}")
        meta = {}

    # 4. Pipedrive
    print("Pipedrive...")
    try:
        pipe = pipedrive.coletar(dt_inicio.isoformat(), dt_fim.isoformat())
    except Exception as e:
        print(f"  ERRO Pipedrive: {e}")
        pipe = {}

    # 5. Monta payload final
    produtos = [
        "aux-moradia", "fies", "fies-suspensao", "direito-medico",
        "inss", "provab", "seguro", "livre-ir", "seg-vida",
    ]
    gastos = {}
    for slug in produtos:
        g = round(gads.get(slug, 0.0), 2)
        m = round(meta.get(slug, 0.0), 2)
        p = pipe.get(slug, {})
        gastos[slug] = {
            "google": g,
            "meta": m,
            "leads_novos": p.get("leads_novos", 0),
            "ganhos": p.get("ganhos", 0),
            "valor_ganhos": round(p.get("valor_ganhos", 0.0), 2),
        }

    saida = {
        "atualizadoEm": datetime.now().isoformat(timespec="seconds"),
        "mesReferencia": mes_ref,
        "tipo": "corrente" if eh_corrente else "fechamento",
        "taxa_usd": round(taxa_usd, 4),
        "fonte_usd": fonte_usd,
        "gastos": gastos,
    }

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    destino = DATA_DIR / ("data.json" if eh_corrente else f"data-fechamento-{mes_ref}.json")
    with destino.open("w", encoding="utf-8") as f:
        json.dump(saida, f, indent=2, ensure_ascii=False)
    print(f"OK → {destino}")

    # Resumo
    total_g = sum(gastos[s]["google"] for s in produtos)
    total_m = sum(gastos[s]["meta"] for s in produtos)
    print(f"Total Google: R$ {total_g:,.2f}  ·  Meta: R$ {total_m:,.2f}  ·  Geral: R$ {total_g+total_m:,.2f}")


if __name__ == "__main__":
    main()
