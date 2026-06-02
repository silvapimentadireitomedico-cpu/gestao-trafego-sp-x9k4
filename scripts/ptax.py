"""Cotação USD→BRL via PTAX BCB (busca os últimos 5 dias úteis até achar)."""
import json
import urllib.request
from datetime import date, timedelta

FALLBACK = 5.20


def _ptax_em(d: date) -> tuple[float, str] | None:
    """Tenta PTAX exatamente em `d`. None se não tiver (fim de semana/feriado)."""
    url = (
        "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/"
        f"CotacaoDolarDia(dataCotacao=@dataCotacao)"
        f"?@dataCotacao='{d.month:02d}-{d.day:02d}-{d.year}'&$format=json"
    )
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            j = json.loads(r.read())
        if j.get("value"):
            return j["value"][0]["cotacaoVenda"], f"BCB {d.day:02d}/{d.month:02d}/{d.year}"
    except Exception:
        pass
    return None


def cotacao(ref: date | None = None) -> tuple[float, str]:
    """Retorna (taxa, fonte) na data ref (ou hoje), retrocedendo até 7 dias úteis.
    Para fechamento de mês, passar ref = último dia do mês fechado.
    """
    base = ref or date.today()
    for i in range(7):
        d = base - timedelta(days=i)
        r = _ptax_em(d)
        if r:
            return r
    return FALLBACK, "fallback"


if __name__ == "__main__":
    import sys
    ref = date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else None
    taxa, fonte = cotacao(ref)
    print(f"{taxa:.4f}  ({fonte})")
