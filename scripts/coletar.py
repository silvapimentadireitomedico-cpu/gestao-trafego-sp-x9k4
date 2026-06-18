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
from datetime import date, datetime, timezone
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
    #    - Mês corrente: usa cotação de hoje (gasto USD do dia)
    #    - Fechamento de mês passado: usa cotação do último dia útil do mês fechado
    #      (assim bate com extratos contábeis e relatório Power BI)
    taxa_usd, fonte_usd = ptax.cotacao(None if eh_corrente else dt_fim)
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

    # 5. Orçamento Diário CONFIGURADO (daily_budget das campanhas/adsets ACTIVE)
    # Só faz sentido pro mês corrente — pra mês fechado, ignora (não há "previsto")
    orc_diario_google = {}
    orc_diario_meta = {}
    if eh_corrente:
        print("Orçamento diário Google...")
        try:
            orc_diario_google = google_ads.coletar_orcamento_diario()
        except Exception as e:
            print(f"  ERRO orc-diario Google: {e}")
        print("Orçamento diário Meta...")
        try:
            orc_diario_meta = meta_ads.coletar_orcamento_diario(taxa_usd)
        except Exception as e:
            print(f"  ERRO orc-diario Meta: {e}")

    # 5.5 Carrega o data.json anterior pra CARRY-FORWARD.
    #     Se uma fonte caiu por completo (ex.: refresh_token do Google expirado), o coletor
    #     NÃO publica zeros silenciosos: reusa o último valor bom e marca a fonte como "erro".
    #     Assim a Action para de zerar o painel quando uma credencial cai, e o frontend
    #     mostra o aviso "não otimize" em cima do número defasado.
    destino = DATA_DIR / ("data.json" if eh_corrente else f"data-fechamento-{mes_ref}.json")
    prev = {}
    if destino.exists():
        try:
            prev = json.loads(destino.read_text(encoding="utf-8"))
        except Exception:
            prev = {}
    prev_mesmo_mes = isinstance(prev, dict) and prev.get("mesReferencia") == mes_ref
    prev_gastos = prev.get("gastos", {}) if prev_mesmo_mes else {}

    # Fonte "erro" = retornou vazio (falha total). Fonte "ok" = trouxe dado.
    fontes = {
        "google": "ok" if gads else "erro",
        "meta": "ok" if meta else "erro",
        "pipedrive": "ok" if pipe else "erro",
    }
    for f, st in fontes.items():
        if st == "erro":
            print(f"  ATENCAO: fonte {f} falhou — carry-forward do ultimo valor bom (sem zerar painel).")

    # 6. Monta payload final
    produtos = [
        "aux-moradia", "fies", "fies-suspensao", "direito-medico",
        "inss", "provab", "seguro", "livre-ir", "seg-vida",
    ]
    gastos = {}
    for slug in produtos:
        prev_slug = prev_gastos.get(slug, {}) if isinstance(prev_gastos.get(slug), dict) else {}
        g = round(gads.get(slug, 0.0), 2)
        m = round(meta.get(slug, 0.0), 2)
        p = pipe.get(slug, {})
        og = round(orc_diario_google.get(slug, 0.0), 2)
        om = round(orc_diario_meta.get(slug, 0.0), 2)

        # Carry-forward por fonte caída (só faz sentido com data.json do mesmo mês)
        if fontes["google"] == "erro" and prev_mesmo_mes:
            g = round(prev_slug.get("google", 0.0), 2)
            og = round(prev_slug.get("orcamento_diario_google", 0.0), 2)
        if fontes["meta"] == "erro" and prev_mesmo_mes:
            m = round(prev_slug.get("meta", 0.0), 2)
            om = round(prev_slug.get("orcamento_diario_meta", 0.0), 2)
        if fontes["pipedrive"] == "erro" and prev_mesmo_mes:
            p = {
                "leads_novos": prev_slug.get("leads_novos", 0),
                "ganhos": prev_slug.get("ganhos", 0),
                "valor_ganhos": prev_slug.get("valor_ganhos", 0.0),
            }

        gastos[slug] = {
            "google": g,
            "meta": m,
            "leads_novos": p.get("leads_novos", 0),
            "ganhos": p.get("ganhos", 0),
            "valor_ganhos": round(p.get("valor_ganhos", 0.0), 2),
            "orcamento_diario_google": og,
            "orcamento_diario_meta": om,
            "orcamento_diario": round(og + om, 2),
        }

    saida = {
        # UTC com sufixo Z — JS converte pra timezone local (BRT) sem ambiguidade
        "atualizadoEm": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "mesReferencia": mes_ref,
        "tipo": "corrente" if eh_corrente else "fechamento",
        "taxa_usd": round(taxa_usd, 4),
        "fonte_usd": fonte_usd,
        "fontes": fontes,
        "gastos": gastos,
    }

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with destino.open("w", encoding="utf-8") as f:
        json.dump(saida, f, indent=2, ensure_ascii=False)
    print(f"OK → {destino}")

    # Resumo
    total_g = sum(gastos[s]["google"] for s in produtos)
    total_m = sum(gastos[s]["meta"] for s in produtos)
    print(f"Total Google: R$ {total_g:,.2f}  ·  Meta: R$ {total_m:,.2f}  ·  Geral: R$ {total_g+total_m:,.2f}")


if __name__ == "__main__":
    main()
