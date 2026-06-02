"""Cotação USD→BRL via PTAX BCB (busca os últimos 5 dias úteis até achar)."""
import json
import urllib.request
from datetime import date, timedelta

FALLBACK = 5.20


def cotacao() -> tuple[float, str]:
    """Retorna (taxa, fonte). Se falhar, fallback 5.20."""
    hoje = date.today()
    for i in range(5):
        d = hoje - timedelta(days=i)
        url = (
            "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/"
            f"CotacaoDolarDia(dataCotacao=@dataCotacao)"
            f"?@dataCotacao='{d.month:02d}-{d.day:02d}-{d.year}'&$format=json"
        )
        try:
            with urllib.request.urlopen(url, timeout=10) as r:
                j = json.loads(r.read())
            if j.get("value"):
                return j["value"][0]["cotacaoVenda"], f"BCB {d.day:02d}/{d.month:02d}"
        except Exception:
            continue
    return FALLBACK, "fallback"


if __name__ == "__main__":
    taxa, fonte = cotacao()
    print(f"{taxa:.4f}  ({fonte})")
