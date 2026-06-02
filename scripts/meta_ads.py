"""Módulo Meta Ads — puxa spend por campanha das 5 contas e mapeia pra produto.

Tokens via env:
  META_ADS_TOKEN       — BM Silva Pimenta Brasil (CA-01, CA-02, CA-03)
  META_ADS_TOKEN_EUA   — BM Silva Pimenta EUA (FIES, AUX)
  META_ADS_TOKEN_LIVRE_IR — BM Livre IR (descontinuado mas API segue ativa)

Conversão USD→BRL injetada pelo coletar.py (taxa do dia).
"""
import json
import os
import urllib.parse
import urllib.request

GRAPH = "https://graph.facebook.com/v23.0"

# act_xxx → (token_var, moeda, regra_de_split)
CONTAS = {
    # Silva Pimenta Brasil (BRL)
    "act_320965166251046": ("META_ADS_TOKEN", "BRL", "by_name_brasil"),
    "act_597293739018501": ("META_ADS_TOKEN", "BRL", "all_seg_vida"),  # CA-02 Securitário: tudo VIDA
    "act_26660757283514357": ("META_ADS_TOKEN", "USD", "by_name_brasil"),  # CA-03 sem produto fixo
    # Silva Pimenta EUA (USD)
    "act_758844583486507": ("META_ADS_TOKEN_EUA", "USD", "all_fies"),
    "act_1271698078245722": ("META_ADS_TOKEN_EUA", "USD", "all_aux"),
    # Livre IR (USD, descontinuado)
    "act_3870149683289741": ("META_ADS_TOKEN_LIVRE_IR", "USD", "all_livre_ir"),
}


def _http_get(url: str) -> dict:
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())


def _slug_por_nome(nome: str) -> str | None:
    """Mapeia nome de campanha (BM SP Brasil CA-01) pra slug de produto."""
    u = nome.upper()
    if "AUXÍLIO MORADIA" in u or "AUXILIO MORADIA" in u or u.startswith("AM "):
        return "aux-moradia"
    if "SUSPENSÃO" in u or "SUSPENSAO" in u:
        return "fies-suspensao"
    if "FIES" in u:
        return "fies"
    if "INSS" in u:
        return "inss"
    if "MAIS MEDICOS" in u or "MAIS MÉDICOS" in u or "PROVAB" in u or "MEDICOS" in u and "MAIS" in u:
        return "provab"
    if "DIREITO MEDICO" in u or "DIREITO MÉDICO" in u or "DEFESA MEDICA" in u:
        return "direito-medico"
    return None


def _campanhas_da_conta(act: str, token: str, since: str, until: str) -> list[tuple[str, float]]:
    """Retorna [(nome_campanha, spend_na_moeda_da_conta)]."""
    params = {
        "access_token": token,
        "fields": "campaign_name,spend",
        "level": "campaign",
        "time_range": json.dumps({"since": since, "until": until}),
        "limit": 500,
    }
    url = f"{GRAPH}/{act}/insights?{urllib.parse.urlencode(params)}"
    body = _http_get(url)
    out = []
    for row in body.get("data") or []:
        nome = row.get("campaign_name") or ""
        spend = float(row.get("spend") or 0)
        out.append((nome, spend))
    return out


def coletar(since: str, until: str, taxa_usd: float = 5.20) -> dict[str, float]:
    """Retorna dict slug → spend em BRL no período (USD convertido pela taxa)."""
    saida: dict[str, float] = {
        "aux-moradia": 0.0, "fies": 0.0, "fies-suspensao": 0.0,
        "direito-medico": 0.0, "inss": 0.0, "provab": 0.0,
        "seguro": 0.0, "livre-ir": 0.0, "seg-vida": 0.0,
    }

    for act, (token_var, moeda, regra) in CONTAS.items():
        token = os.environ.get(token_var)
        if not token:
            print(f"  WARN Meta: {token_var} não configurado (pulando {act})")
            continue
        try:
            campanhas = _campanhas_da_conta(act, token, since, until)
        except Exception as e:
            print(f"  WARN Meta {act}: {e}")
            continue

        for nome, spend in campanhas:
            valor_brl = spend if moeda == "BRL" else spend * taxa_usd

            if regra == "all_aux":
                saida["aux-moradia"] += valor_brl
            elif regra == "all_fies":
                saida["fies"] += valor_brl
            elif regra == "all_seg_vida":
                saida["seg-vida"] += valor_brl
            elif regra == "all_livre_ir":
                saida["livre-ir"] += valor_brl
            elif regra == "by_name_brasil":
                slug = _slug_por_nome(nome)
                if slug:
                    saida[slug] += valor_brl
                else:
                    print(f"  INFO Meta {act}: campanha não mapeada: {nome!r} R$ {valor_brl:.2f}")
    return saida


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Uso: python meta_ads.py YYYY-MM-DD YYYY-MM-DD [taxa_usd=5.20]")
        sys.exit(1)
    taxa = float(sys.argv[3]) if len(sys.argv) > 3 else 5.20
    print(json.dumps(coletar(sys.argv[1], sys.argv[2], taxa), indent=2))
