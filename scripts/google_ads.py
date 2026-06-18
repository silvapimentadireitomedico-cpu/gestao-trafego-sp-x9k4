"""Módulo Google Ads — puxa custo por produto e separa NEG VIDA do Seguro.

Usa o SDK google-ads via env vars:
  GOOGLE_ADS_DEVELOPER_TOKEN, GOOGLE_ADS_CLIENT_ID, GOOGLE_ADS_CLIENT_SECRET,
  GOOGLE_ADS_REFRESH_TOKEN, GOOGLE_ADS_LOGIN_CUSTOMER_ID
"""
import os
from google.ads.googleads.client import GoogleAdsClient


# customer_id sem hifens → slug do produto no dashboard
CONTAS_DIRETAS = {
    "3560859574": "aux-moradia",
    "5313139497": "fies",
    "6351554556": "direito-medico",
    "3237663933": "livre-ir",
}

# Contas que precisam split campanha-a-campanha (VIDA vs SEGURO/VEICULAR)
# Resultado vai pra produtos 'seguro' (não-VIDA) e 'seg-vida' (VIDA).
CONTAS_SEGURO = ["1301598996", "2903149800"]

# MCC que enxerga as contas do lado MÉDICO (Aux/FIES/Direito). Think Lab.
# As contas diretas vivem sob esse MCC; se o login_customer_id do ambiente
# apontar pra outro MCC (ex.: o de Seguro), elas vinham com custo 0.
MCC_MEDICO = "9025188297"


def _client(login_customer_id: str | None = None) -> GoogleAdsClient:
    cfg = {
        "developer_token": os.environ["GOOGLE_ADS_DEVELOPER_TOKEN"],
        "client_id": os.environ["GOOGLE_ADS_CLIENT_ID"],
        "client_secret": os.environ["GOOGLE_ADS_CLIENT_SECRET"],
        "refresh_token": os.environ["GOOGLE_ADS_REFRESH_TOKEN"],
        "login_customer_id": login_customer_id or os.environ["GOOGLE_ADS_LOGIN_CUSTOMER_ID"],
        "use_proto_plus": True,
    }
    return GoogleAdsClient.load_from_dict(cfg)


def _date_clause(date_range: str, since: str | None, until: str | None) -> str:
    if since and until:
        return f"segments.date BETWEEN '{since}' AND '{until}'"
    return f"segments.date DURING {date_range}"


def _custo_conta(client: GoogleAdsClient, customer_id: str, date_clause: str) -> float:
    """Soma cost_micros da conta no período."""
    svc = client.get_service("GoogleAdsService")
    query = f"""
        SELECT metrics.cost_micros
        FROM customer
        WHERE {date_clause}
    """
    total = 0.0
    for row in svc.search(customer_id=customer_id, query=query):
        total += (row.metrics.cost_micros or 0) / 1_000_000
    return total


def _custo_campanhas(client: GoogleAdsClient, customer_id: str, date_clause: str) -> list[tuple[str, float]]:
    """Retorna [(nome_campanha, custo_brl)]."""
    svc = client.get_service("GoogleAdsService")
    query = f"""
        SELECT campaign.name, metrics.cost_micros
        FROM campaign
        WHERE campaign.status != 'REMOVED'
          AND {date_clause}
          AND metrics.cost_micros > 0
    """
    out = []
    for row in svc.search(customer_id=customer_id, query=query):
        out.append((row.campaign.name or "", (row.metrics.cost_micros or 0) / 1_000_000))
    return out


def coletar(date_range: str = "THIS_MONTH", since: str | None = None, until: str | None = None) -> dict[str, float]:
    """Retorna dict slug → custo BRL no período.
    date_range padrão é THIS_MONTH (Google Ads aceita LAST_MONTH, LAST_30_DAYS, etc).
    Se since/until forem informados, usa BETWEEN.
    """
    client = _client()
    client_med = _client(MCC_MEDICO)   # contas do lado médico vivem sob esse MCC
    date_clause = _date_clause(date_range, since, until)

    saida: dict[str, float] = {slug: 0.0 for slug in CONTAS_DIRETAS.values()}
    saida["seguro"] = 0.0
    saida["seg-vida"] = 0.0

    contas = 0
    erros = 0

    # Contas diretas (via MCC médico)
    for cid, slug in CONTAS_DIRETAS.items():
        contas += 1
        try:
            saida[slug] += _custo_conta(client_med, cid, date_clause)
        except Exception as e:
            erros += 1
            print(f"  WARN Google Ads {slug} ({cid}): {e}")

    # Contas seguro com split por nome de campanha
    for cid in CONTAS_SEGURO:
        contas += 1
        try:
            for nome, custo in _custo_campanhas(client, cid, date_clause):
                if "VIDA" in nome.upper():
                    saida["seg-vida"] += custo
                else:
                    saida["seguro"] += custo
        except Exception as e:
            erros += 1
            print(f"  WARN Google Ads seguro ({cid}): {e}")

    # Se TODAS as contas falharam, é credencial/token (não é gasto zero real).
    # Levanta exceção pra coletar.py NÃO publicar um painel inteiro zerado e silencioso.
    if contas and erros == contas:
        raise RuntimeError(
            f"Google Ads: todas as {contas} contas falharam — credencial/refresh_token provável. "
            "NÃO publicando zeros."
        )

    return saida


def _budgets_diarios(client: GoogleAdsClient, customer_id: str) -> list[tuple[str, str, float]]:
    """Retorna [(nome_campanha, budget_id, daily_brl)] das campanhas ENABLED.
    Budget no Google Ads pode ser COMPARTILHADO — então deduplica por budget_id depois.
    """
    svc = client.get_service("GoogleAdsService")
    query = """
        SELECT
            campaign.name,
            campaign.status,
            campaign_budget.id,
            campaign_budget.amount_micros,
            campaign_budget.period
        FROM campaign
        WHERE campaign.status = 'ENABLED'
    """
    out = []
    for row in svc.search(customer_id=customer_id, query=query):
        # period: DAILY ou CUSTOM_PERIOD. Só conta DAILY (CUSTOM_PERIOD ignorado).
        period_name = row.campaign_budget.period.name if row.campaign_budget.period else ""
        if period_name != "DAILY":
            continue
        nome = row.campaign.name or ""
        bid = str(row.campaign_budget.id)
        daily = (row.campaign_budget.amount_micros or 0) / 1_000_000
        out.append((nome, bid, daily))
    return out


def coletar_orcamento_diario() -> dict[str, float]:
    """Soma daily_budget das campanhas ENABLED por produto.
    Deduplica budgets compartilhados.
    """
    saida: dict[str, float] = {slug: 0.0 for slug in CONTAS_DIRETAS.values()}
    saida["seguro"] = 0.0
    saida["seg-vida"] = 0.0

    client = _client()
    client_med = _client(MCC_MEDICO)

    contas = 0
    erros = 0

    # Contas diretas: budget vai todo pro produto da conta (via MCC médico)
    for cid, slug in CONTAS_DIRETAS.items():
        contas += 1
        try:
            vistos = set()  # dedupe budgets dentro da MESMA conta
            for nome, bid, daily in _budgets_diarios(client_med, cid):
                if bid in vistos:
                    continue
                vistos.add(bid)
                saida[slug] += daily
        except Exception as e:
            erros += 1
            print(f"  WARN Google orc-diario {slug} ({cid}): {e}")

    # Contas seguro: split por nome (VIDA → seg-vida, resto → seguro)
    for cid in CONTAS_SEGURO:
        contas += 1
        try:
            vistos = set()
            for nome, bid, daily in _budgets_diarios(client, cid):
                if bid in vistos:
                    continue
                vistos.add(bid)
                slug = "seg-vida" if "VIDA" in nome.upper() else "seguro"
                saida[slug] += daily
        except Exception as e:
            erros += 1
            print(f"  WARN Google orc-diario seguro ({cid}): {e}")

    if contas and erros == contas:
        raise RuntimeError("Google Ads orc-diário: todas as contas falharam — credencial provável.")

    return saida


if __name__ == "__main__":
    import json
    import sys
    if len(sys.argv) >= 2 and sys.argv[1] == "--orc":
        print(json.dumps(coletar_orcamento_diario(), indent=2))
    else:
        arg = sys.argv[1] if len(sys.argv) > 1 else "THIS_MONTH"
        if "-" in arg and len(arg) == 10:
            print(json.dumps(coletar(since=sys.argv[1], until=sys.argv[2]), indent=2))
        else:
            print(json.dumps(coletar(date_range=arg), indent=2))
