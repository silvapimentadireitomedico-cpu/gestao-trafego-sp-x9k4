"""Coletor da RITA — dump granular ad-a-ad pra alimentar o relatório da Rita na nuvem.

Diferente do coletar.py (que agrega gasto por produto pro painel de orçamento),
este aqui DUMPA os dados GRANULARES que a skill rita-relatorios precisa pra escrever
o relatório de analista sênior (campanha / ad group / keyword / search term / ad,
janelas 30/14/7 dias, rankings de qualidade Meta, QS Google, gate de aprovação,
Pipedrive com perdas-por-motivo). A Rita na nuvem só LÊ este JSON, nunca toca a API.

Arquitetura (decidida 19/06/2026): a GitHub Action já tem os tokens (secrets);
ela roda este coletor e commita data/rita/<produto>.json. A Rita (read-only) lê o JSON.
Sem cópia nova de token em lugar nenhum.

Reusa auth/infra dos módulos vizinhos:
  google_ads._client / MCC_MEDICO   (SDK Google Ads + roteamento por MCC)
  meta_ads.GRAPH / _http_get        (Graph API via urllib)
  pipedrive._token / _base_v2       (Pipedrive v2)

Uso:
  python scripts/rita_collector.py                 # todos os produtos
  python scripts/rita_collector.py aux-moradia     # um produto
  python scripts/rita_collector.py --produtos fies,direito-medico

Gera (relativo à raiz do repo):
  data/rita/<produto>.json   (um por produto)
  data/rita/_index.json      (lista + timestamp)
"""
import argparse
import json
import os
import sys
import urllib.parse
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import google_ads
import meta_ads
import pipedrive
import ptax

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data" / "rita"

# Janelas (dias). until = ontem (dia de hoje fica incompleto e contamina a leitura).
JANELAS = [30, 14, 7]

# action_types do Meta que importam pra lead-gen jurídico (o resto vira ruído no JSON)
META_ACTIONS_RELEVANTES = {
    "lead",
    "onsite_conversion.lead_grouped",
    "offsite_conversion.fb_pixel_lead",
    "onsite_conversion.messaging_conversation_started_7d",
    "onsite_conversion.messaging_first_reply",
    "link_click",
    "landing_page_view",
    "post_engagement",
}

# ---------------------------------------------------------------------------
# Mapa produto → contas (espelha rita-relatorios/SKILL.md §3 + meta_ads.CONTAS)
# ---------------------------------------------------------------------------
PRODUTOS = {
    "aux-moradia": {
        "rotulo": "Auxílio Moradia",
        "cliente": "silva-pimenta",
        "google": [
            {"customer_id": "3560859574", "login": "medico", "nome": "LP - Auxílio Moradia"},
        ],
        "meta": [
            {"act": "act_320965166251046", "token_var": "META_ADS_TOKEN", "moeda": "BRL",
             "bm": "SP Brasil", "filtro_slug": ["aux-moradia"]},
            {"act": "act_1271698078245722", "token_var": "META_ADS_TOKEN_EUA", "moeda": "USD",
             "bm": "SP EUA", "filtro_slug": None},  # conta dedicada → tudo
        ],
        "pipedrive_funis": {1: "Auxílio Moradia"},
    },
    "fies": {
        "rotulo": "FIES (Abatimento + Suspensão)",
        "cliente": "silva-pimenta",
        "google": [
            {"customer_id": "5313139497", "login": "medico", "nome": "Silva Pimenta - [FIES]"},
        ],
        "meta": [
            {"act": "act_320965166251046", "token_var": "META_ADS_TOKEN", "moeda": "BRL",
             "bm": "SP Brasil", "filtro_slug": ["fies", "fies-suspensao"]},
            {"act": "act_758844583486507", "token_var": "META_ADS_TOKEN_EUA", "moeda": "USD",
             "bm": "SP EUA", "filtro_slug": None},
        ],
        "pipedrive_funis": {2: "FIES Abatimento", 4: "FIES Suspensão"},
    },
    "direito-medico": {
        "rotulo": "Direito Médico (Defesa)",
        "cliente": "silva-pimenta",
        "google": [
            {"customer_id": "6351554556", "login": "medico", "nome": "LP | DIREITO MÉDICO"},
        ],
        "meta": [
            {"act": "act_320965166251046", "token_var": "META_ADS_TOKEN", "moeda": "BRL",
             "bm": "SP Brasil", "filtro_slug": ["direito-medico"]},
        ],
        "pipedrive_funis": {6: "Direito Médico"},
    },
    "seguro": {
        "rotulo": "Seguro (Magalhães Gomes)",
        "cliente": "magalhaes-gomes",
        "google": [
            {"customer_id": "1301598996", "login": "default", "nome": "MG Seguro Institucional",
             "excluir_vida": True},
            {"customer_id": "2903149800", "login": "default", "nome": "MG Seguro Contingência",
             "excluir_vida": True},
        ],
        "meta": [],  # Meta do Seguro a confirmar (ver references/seguro.md)
        "pipedrive_funis": {3: "Seguro Geral (não-VIDA)"},
    },
}


def _janelas_datas(hoje: date) -> dict:
    """{ '30d': (since, until), ... } com until=ontem, datas ISO."""
    until = hoje - timedelta(days=1)
    out = {}
    for n in JANELAS:
        since = hoje - timedelta(days=n)
        out[f"{n}d"] = (since.isoformat(), until.isoformat())
    return out


def _num(v) -> float:
    try:
        return float(v)
    except (TypeError, ValueError):
        return 0.0


# ===========================================================================
# GOOGLE ADS (granular)
# ===========================================================================

def _g_client(login: str):
    if login == "medico":
        return google_ads._client(google_ads.MCC_MEDICO)
    return google_ads._client()


def _g_run(client, customer_id: str, query: str) -> list:
    svc = client.get_service("GoogleAdsService")
    return list(svc.search(customer_id=customer_id, query=query))


def _g_campanhas(client, cid, since, until):
    q = f"""
        SELECT campaign.name, campaign.status,
               metrics.cost_micros, metrics.impressions, metrics.clicks,
               metrics.ctr, metrics.average_cpc, metrics.conversions,
               metrics.cost_per_conversion
        FROM campaign
        WHERE campaign.status != 'REMOVED'
          AND segments.date BETWEEN '{since}' AND '{until}'
          AND metrics.impressions > 0
        ORDER BY metrics.cost_micros DESC
    """
    out = []
    for r in _g_run(client, cid, q):
        out.append({
            "campanha": r.campaign.name,
            "status": r.campaign.status.name,
            "custo": round(r.metrics.cost_micros / 1e6, 2),
            "impressoes": r.metrics.impressions,
            "cliques": r.metrics.clicks,
            "ctr": round(r.metrics.ctr * 100, 2),
            "cpc_medio": round(r.metrics.average_cpc / 1e6, 2),
            "conversoes": round(r.metrics.conversions, 2),
            "custo_por_conv": round(r.metrics.cost_per_conversion / 1e6, 2),
        })
    return out


def _g_ad_groups(client, cid, since, until):
    q = f"""
        SELECT ad_group.name, campaign.name, ad_group.status,
               metrics.cost_micros, metrics.impressions, metrics.clicks,
               metrics.ctr, metrics.conversions, metrics.cost_per_conversion
        FROM ad_group
        WHERE ad_group.status != 'REMOVED'
          AND segments.date BETWEEN '{since}' AND '{until}'
          AND metrics.impressions > 0
        ORDER BY metrics.cost_micros DESC
    """
    out = []
    for r in _g_run(client, cid, q):
        out.append({
            "ad_group": r.ad_group.name,
            "campanha": r.campaign.name,
            "status": r.ad_group.status.name,
            "custo": round(r.metrics.cost_micros / 1e6, 2),
            "impressoes": r.metrics.impressions,
            "cliques": r.metrics.clicks,
            "ctr": round(r.metrics.ctr * 100, 2),
            "conversoes": round(r.metrics.conversions, 2),
            "custo_por_conv": round(r.metrics.cost_per_conversion / 1e6, 2),
        })
    return out


def _g_keywords(client, cid, since, until, limit=60):
    q = f"""
        SELECT ad_group_criterion.keyword.text,
               ad_group_criterion.keyword.match_type,
               ad_group_criterion.status,
               ad_group_criterion.quality_info.quality_score,
               ad_group.name, campaign.name,
               metrics.impressions, metrics.clicks, metrics.cost_micros,
               metrics.conversions, metrics.ctr, metrics.average_cpc
        FROM keyword_view
        WHERE ad_group_criterion.status != 'REMOVED'
          AND segments.date BETWEEN '{since}' AND '{until}'
          AND metrics.impressions > 0
        ORDER BY metrics.cost_micros DESC
        LIMIT {limit}
    """
    out = []
    for r in _g_run(client, cid, q):
        out.append({
            "keyword": r.ad_group_criterion.keyword.text,
            "match": r.ad_group_criterion.keyword.match_type.name,
            "quality_score": r.ad_group_criterion.quality_info.quality_score or None,
            "ad_group": r.ad_group.name,
            "campanha": r.campaign.name,
            "impressoes": r.metrics.impressions,
            "cliques": r.metrics.clicks,
            "custo": round(r.metrics.cost_micros / 1e6, 2),
            "conversoes": round(r.metrics.conversions, 2),
            "ctr": round(r.metrics.ctr * 100, 2),
            "cpc_medio": round(r.metrics.average_cpc / 1e6, 2),
        })
    return out


def _g_search_terms(client, cid, since, until, limit=60):
    q = f"""
        SELECT search_term_view.search_term, search_term_view.status,
               campaign.name, ad_group.name,
               metrics.impressions, metrics.clicks, metrics.cost_micros,
               metrics.conversions, metrics.ctr
        FROM search_term_view
        WHERE segments.date BETWEEN '{since}' AND '{until}'
          AND metrics.impressions > 0
        ORDER BY metrics.cost_micros DESC
        LIMIT {limit}
    """
    out = []
    for r in _g_run(client, cid, q):
        out.append({
            "termo": r.search_term_view.search_term,
            "status": r.search_term_view.status.name,
            "campanha": r.campaign.name,
            "ad_group": r.ad_group.name,
            "impressoes": r.metrics.impressions,
            "cliques": r.metrics.clicks,
            "custo": round(r.metrics.cost_micros / 1e6, 2),
            "conversoes": round(r.metrics.conversions, 2),
            "ctr": round(r.metrics.ctr * 100, 2),
        })
    return out


def _g_ads_gate(client, cid):
    """GATE: status de aprovação dos anúncios (DISAPPROVED = morto, métrica vira ruído)."""
    q = """
        SELECT ad_group_ad.ad.id, ad_group_ad.ad.name, ad_group_ad.status,
               ad_group_ad.policy_summary.approval_status,
               ad_group_ad.policy_summary.review_status,
               ad_group.name, campaign.name
        FROM ad_group_ad
        WHERE ad_group_ad.status = 'ENABLED'
    """
    out = []
    for r in _g_run(client, cid, q):
        aprov = r.ad_group_ad.policy_summary.approval_status.name
        out.append({
            "ad_id": str(r.ad_group_ad.ad.id),
            "ad": r.ad_group_ad.ad.name or "(sem nome)",
            "campanha": r.campaign.name,
            "ad_group": r.ad_group.name,
            "aprovacao": aprov,
            "review": r.ad_group_ad.policy_summary.review_status.name,
        })
    return out


def _excluir_vida(linhas: list, key="campanha") -> list:
    return [x for x in linhas if "VIDA" not in (x.get(key) or "").upper()]


def coletar_google(prod_cfg: dict, janelas: dict) -> dict:
    contas_out = []
    erros = []
    for conta in prod_cfg["google"]:
        cid = conta["customer_id"]
        excl_vida = conta.get("excluir_vida", False)
        try:
            client = _g_client(conta["login"])
        except Exception as e:
            erros.append(f"Google {cid}: auth falhou: {e}")
            continue

        bloco = {"customer_id": cid, "nome": conta["nome"], "janelas": {}}
        # GATE (não depende de janela)
        try:
            gate = _g_ads_gate(client, cid)
            if excl_vida:
                gate = _excluir_vida(gate)
            bloco["ads_gate"] = gate
            bloco["ads_reprovados"] = [a for a in gate if a["aprovacao"] not in ("APPROVED", "APPROVED_LIMITED", "UNKNOWN")]
        except Exception as e:
            erros.append(f"Google {cid} gate: {e}")
            bloco["ads_gate"] = []
            bloco["ads_reprovados"] = []

        for jan, (since, until) in janelas.items():
            try:
                camp = _g_campanhas(client, cid, since, until)
                ag = _g_ad_groups(client, cid, since, until)
                kw = _g_keywords(client, cid, since, until)
                st = _g_search_terms(client, cid, since, until)
                if excl_vida:
                    camp, ag, kw, st = (_excluir_vida(x) for x in (camp, ag, kw, st))
                bloco["janelas"][jan] = {
                    "periodo": f"{since} a {until}",
                    "totais": _g_totais(camp),
                    "campanhas": camp,
                    "ad_groups": ag,
                    "keywords": kw,
                    "search_terms_top": st,
                }
            except Exception as e:
                erros.append(f"Google {cid} {jan}: {e}")
                bloco["janelas"][jan] = {"periodo": f"{since} a {until}", "erro": str(e)}
        contas_out.append(bloco)
    return {"contas": contas_out, "erros": erros}


def _g_totais(campanhas: list) -> dict:
    custo = sum(c["custo"] for c in campanhas)
    cliques = sum(c["cliques"] for c in campanhas)
    impr = sum(c["impressoes"] for c in campanhas)
    conv = sum(c["conversoes"] for c in campanhas)
    return {
        "custo": round(custo, 2),
        "impressoes": impr,
        "cliques": cliques,
        "conversoes": round(conv, 2),
        "ctr": round((cliques / impr * 100) if impr else 0, 2),
        "cpc_medio": round((custo / cliques) if cliques else 0, 2),
        "custo_por_conv": round((custo / conv) if conv else 0, 2),
    }


# ===========================================================================
# META ADS (granular: insights level=ad + rankings + gate de status)
# ===========================================================================

def _meta_token(token_var: str):
    return os.environ.get(token_var)


def _meta_insights_ad(act, token, since, until):
    """Insights por anúncio com rankings de qualidade. Pagina via after."""
    fields = ("campaign_name,adset_name,ad_name,ad_id,spend,impressions,reach,frequency,"
              "clicks,ctr,cpc,actions,cost_per_action_type,quality_ranking,"
              "engagement_rate_ranking,conversion_rate_ranking")
    params = {
        "access_token": token, "level": "ad", "fields": fields,
        "time_range": json.dumps({"since": since, "until": until}),
        "limit": 200,
    }
    url = f"{meta_ads.GRAPH}/{act}/insights?{urllib.parse.urlencode(params)}"
    linhas = []
    while url:
        body = meta_ads._http_get(url)
        linhas.extend(body.get("data") or [])
        url = ((body.get("paging") or {}).get("next"))
    return linhas


def _meta_status_ads(act, token):
    """GATE: anúncios com effective_status problemático (WITH_ISSUES / DISAPPROVED)."""
    params = {
        "access_token": token,
        "fields": "name,effective_status,configured_status,campaign{name}",
        "limit": 500,
    }
    url = f"{meta_ads.GRAPH}/{act}/ads?{urllib.parse.urlencode(params)}"
    out = []
    while url:
        body = meta_ads._http_get(url)
        for r in body.get("data") or []:
            out.append({
                "ad": r.get("name") or "",
                "campanha": (r.get("campaign") or {}).get("name") or "",
                "effective_status": r.get("effective_status") or "",
                "configured_status": r.get("configured_status") or "",
            })
        url = ((body.get("paging") or {}).get("next"))
    return out


def _actions_to_dict(lst, relevantes=True):
    out = {}
    for a in lst or []:
        t = a.get("action_type")
        if relevantes and t not in META_ACTIONS_RELEVANTES:
            continue
        out[t] = _num(a.get("value"))
    return out


def _meta_match_filtro(campaign_name: str, filtro_slug) -> bool:
    if filtro_slug is None:
        return True
    return meta_ads._slug_por_nome(campaign_name) in filtro_slug


def coletar_meta(prod_cfg: dict, janelas: dict, taxa_usd: float) -> dict:
    contas_out = []
    erros = []
    for conta in prod_cfg["meta"]:
        act = conta["act"]
        token = _meta_token(conta["token_var"])
        if not token:
            erros.append(f"Meta {act}: token {conta['token_var']} ausente")
            continue
        moeda = conta["moeda"]
        fx = taxa_usd if moeda == "USD" else 1.0
        filtro = conta["filtro_slug"]

        bloco = {"act": act, "bm": conta["bm"], "moeda": moeda, "janelas": {}}

        # GATE de status (não depende de janela)
        try:
            status = _meta_status_ads(act, token)
            status = [s for s in status if _meta_match_filtro(s["campanha"], filtro)]
            bloco["ads_com_problema"] = [
                s for s in status
                if s["effective_status"] not in ("ACTIVE", "PAUSED", "ADSET_PAUSED",
                                                 "CAMPAIGN_PAUSED", "ARCHIVED", "DELETED",
                                                 "IN_PROCESS", "PENDING_REVIEW")
            ]
        except Exception as e:
            erros.append(f"Meta {act} status: {e}")
            bloco["ads_com_problema"] = []

        for jan, (since, until) in janelas.items():
            try:
                linhas = _meta_insights_ad(act, token, since, until)
                ads = []
                for r in linhas:
                    if not _meta_match_filtro(r.get("campaign_name") or "", filtro):
                        continue
                    spend = _num(r.get("spend")) * fx
                    ads.append({
                        "campanha": r.get("campaign_name") or "",
                        "adset": r.get("adset_name") or "",
                        "ad": r.get("ad_name") or "",
                        "ad_id": r.get("ad_id") or "",
                        "gasto": round(spend, 2),
                        "impressoes": int(_num(r.get("impressions"))),
                        "alcance": int(_num(r.get("reach"))),
                        "frequencia": round(_num(r.get("frequency")), 2),
                        "cliques": int(_num(r.get("clicks"))),
                        "ctr": round(_num(r.get("ctr")), 2),
                        "cpc": round(_num(r.get("cpc")) * fx, 2),
                        "quality_ranking": r.get("quality_ranking") or "UNKNOWN",
                        "engagement_rate_ranking": r.get("engagement_rate_ranking") or "UNKNOWN",
                        "conversion_rate_ranking": r.get("conversion_rate_ranking") or "UNKNOWN",
                        "actions": _actions_to_dict(r.get("actions")),
                        "custo_por_acao": {k: round(v * fx, 2)
                                           for k, v in _actions_to_dict(r.get("cost_per_action_type")).items()},
                    })
                ads.sort(key=lambda x: x["gasto"], reverse=True)
                bloco["janelas"][jan] = {
                    "periodo": f"{since} a {until}",
                    "totais": _meta_totais(ads),
                    "ads": ads,
                }
            except Exception as e:
                erros.append(f"Meta {act} {jan}: {e}")
                bloco["janelas"][jan] = {"periodo": f"{since} a {until}", "erro": str(e)}
        contas_out.append(bloco)
    return {"contas": contas_out, "erros": erros, "taxa_usd": taxa_usd}


def _meta_totais(ads: list) -> dict:
    gasto = sum(a["gasto"] for a in ads)
    cliques = sum(a["cliques"] for a in ads)
    impr = sum(a["impressoes"] for a in ads)
    leads = sum((a["actions"].get("lead", 0)
                 + a["actions"].get("onsite_conversion.lead_grouped", 0)
                 + a["actions"].get("offsite_conversion.fb_pixel_lead", 0)
                 + a["actions"].get("onsite_conversion.messaging_conversation_started_7d", 0))
                for a in ads)
    return {
        "gasto": round(gasto, 2),
        "impressoes": impr,
        "cliques": cliques,
        "ctr": round((cliques / impr * 100) if impr else 0, 2),
        "leads_aprox": round(leads, 1),
        "cpl_aprox": round((gasto / leads) if leads else 0, 2),
    }


# ===========================================================================
# PIPEDRIVE (granular: cohort por add_time, status open/won/lost, perdas-por-motivo)
# ===========================================================================

def _pd_deals_funil(pipeline_id: int) -> list:
    """Todos os deals de um funil (paginado v2), com campos pra cohort/perda."""
    token = pipedrive._token()
    base = pipedrive._base_v2()
    cursor = None
    out = []
    while True:
        params = {"api_token": token, "pipeline_id": pipeline_id, "limit": 500}
        if cursor:
            params["cursor"] = cursor
        url = f"{base}/deals?{urllib.parse.urlencode(params)}"
        body = pipedrive._http_get(url)
        out.extend(body.get("data") or [])
        cursor = (body.get("additional_data") or {}).get("next_cursor")
        if not cursor:
            break
    return out


def _pd_lost_reason_map() -> dict:
    """id → label dos motivos de perda (se o endpoint existir; senão usa o texto cru)."""
    try:
        token = pipedrive._token()
        url = f"{pipedrive._base_v1()}/lostReasons?api_token={token}&limit=500"
        data = pipedrive._http_get(url).get("data") or []
        return {str(r.get("id")): r.get("name") for r in data if r.get("id")}
    except Exception:
        return {}


def coletar_pipedrive(prod_cfg: dict, janelas: dict, hoje: date) -> dict:
    funis = prod_cfg["pipedrive_funis"]
    # janela mais larga (30d) define o corte de busca; bucketiza as 3 em Python
    inicios = {jan: datetime.fromisoformat(s + "T00:00:00-03:00")
               for jan, (s, _u) in janelas.items()}
    fim = datetime.fromisoformat(janelas[f"{max(JANELAS)}d"][1] + "T23:59:59-03:00")

    campo_seguro = None
    try:
        campo_seguro = pipedrive._campo_tipo_seguro()
    except Exception:
        pass
    motivos_map = _pd_lost_reason_map()

    saida = {"funis": {}, "erros": []}
    for pid, label in funis.items():
        try:
            deals = _pd_deals_funil(pid)
        except Exception as e:
            saida["erros"].append(f"Pipedrive funil {pid}: {e}")
            continue

        jan_stats = {jan: {"leads_novos": 0, "abertos": 0, "ganhos": 0,
                           "valor_ganhos": 0.0, "perdidos": 0, "perdas_por_motivo": {}}
                     for jan in janelas}

        for d in deals:
            # Seguro: só não-VIDA neste produto
            if pid == 3 and campo_seguro:
                if pipedrive._tipo_seguro_do_deal(d, campo_seguro) == "vida":
                    continue
            add_time = d.get("add_time")
            if not add_time:
                continue
            add_dt = datetime.fromisoformat(add_time.replace("Z", "+00:00"))
            if not (inicios[f"{max(JANELAS)}d"] <= add_dt <= fim):
                continue
            status = d.get("status")
            valor = _num(d.get("value"))
            motivo = d.get("lost_reason")
            if not motivo and d.get("lost_reason_id"):
                motivo = motivos_map.get(str(d.get("lost_reason_id")))
            motivo = (motivo or "(sem motivo)").strip()

            for jan in janelas:
                if add_dt >= inicios[jan]:
                    s = jan_stats[jan]
                    s["leads_novos"] += 1
                    if status == "won":
                        s["ganhos"] += 1
                        s["valor_ganhos"] += valor
                    elif status == "lost":
                        s["perdidos"] += 1
                        s["perdas_por_motivo"][motivo] = s["perdas_por_motivo"].get(motivo, 0) + 1
                    else:
                        s["abertos"] += 1

        for jan in jan_stats:
            jan_stats[jan]["valor_ganhos"] = round(jan_stats[jan]["valor_ganhos"], 2)
            jan_stats[jan]["periodo"] = f"{janelas[jan][0]} a {janelas[jan][1]}"
        saida["funis"][label] = {"pipeline_id": pid, "janelas": jan_stats}
    return saida


# ===========================================================================
# ORQUESTRAÇÃO
# ===========================================================================

def coletar_produto(slug: str, janelas: dict, taxa_usd: float, hoje: date) -> dict:
    cfg = PRODUTOS[slug]
    print(f"  Google...", flush=True)
    g = coletar_google(cfg, janelas)
    print(f"  Meta...", flush=True)
    m = coletar_meta(cfg, janelas, taxa_usd) if cfg["meta"] else {"contas": [], "erros": [], "nota": "Meta não mapeado pra este produto"}
    print(f"  Pipedrive...", flush=True)
    p = coletar_pipedrive(cfg, janelas, hoje)

    erros = (g.get("erros") or []) + (m.get("erros") or []) + (p.get("erros") or [])
    return {
        "produto": slug,
        "rotulo": cfg["rotulo"],
        "cliente": cfg["cliente"],
        "_leia_me": {
            "para": "Rita (skill rita-relatorios). Você é READ-ONLY: este JSON é a única fonte, "
                    "NÃO chame API. Todo número aqui veio da API na coleta (verificação em cadeia OK).",
            "pipedrive_semantica": "Visão de COHORT por add_time: leads_novos = leads que ENTRARAM na "
                "janela; abertos/ganhos/perdidos = situação ATUAL desses mesmos leads; valor_ganhos só "
                "dos won. Difere do painel de orçamento (que conta won por won_time). Use isto pra "
                "qualidade da safra da campanha. perdas_por_motivo é a seção 5.1: LIXO=público errado, "
                "AÇÃO INVIÁVEL/INVIÁVEL=expectativa criada no anúncio, VALOR BAIXO=qualificação, "
                "SEM RESPOSTA=velocidade SDR.",
            "gates": "Google ads_reprovados = approval != APPROVED/APPROVED_LIMITED (morto, métrica vira "
                "ruído). Meta ads_com_problema = effective_status fora de ACTIVE/PAUSED/etc (WITH_ISSUES, "
                "DISAPPROVED). Meta quality_ranking/conversion_rate_ranking podem vir UNKNOWN em campanha "
                "de mensagem/CTWA ou volume baixo: isso é o valor real da API, não otimize ranking nesse caso.",
            "lacunas_v1": "NÃO inclui: (1) quebra de perdas por 'número da campanha' (campo da pessoa) "
                "dentro do funil, cruzamento ainda calibrando pós-16/06; (2) checagem de número de WhatsApp "
                "vivo na LP (gate 2 de tracking exige ler a LP). Sinalize estes dois como pendência no relatório.",
            "moeda": "Valores de conta USD já convertidos pra BRL pela taxa_usd. Conv/leads são contagem.",
        },
        "atualizadoEm": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "janelas_def": {jan: {"periodo": f"{s} a {u}", "dias": int(jan[:-1])}
                        for jan, (s, u) in janelas.items()},
        "taxa_usd": round(taxa_usd, 4),
        "fontes_ok": {"google": not g.get("erros"), "meta": not m.get("erros") or not cfg["meta"],
                      "pipedrive": not p.get("erros")},
        "google": g,
        "meta": m,
        "pipedrive": p,
        "erros": erros,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("produto", nargs="?", help="slug único (aux-moradia, fies, direito-medico, seguro)")
    ap.add_argument("--produtos", help="lista separada por vírgula")
    a = ap.parse_args()

    if a.produto:
        alvos = [a.produto]
    elif a.produtos:
        alvos = [x.strip() for x in a.produtos.split(",")]
    else:
        alvos = list(PRODUTOS.keys())

    invalidos = [x for x in alvos if x not in PRODUTOS]
    if invalidos:
        print(f"ERRO: produto(s) desconhecido(s): {invalidos}. Válidos: {list(PRODUTOS)}")
        return 2

    hoje = date.today()
    janelas = _janelas_datas(hoje)
    try:
        taxa_usd, fonte_usd = ptax.cotacao(None)
    except Exception as e:
        print(f"  WARN PTAX falhou ({e}); usando 5.20")
        taxa_usd, fonte_usd = 5.20, "fallback"

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    print(f"== RITA collector · {hoje} · janelas {list(janelas)} · USD {taxa_usd:.4f} ({fonte_usd}) ==")

    indice = []
    for slug in alvos:
        print(f"[{slug}]", flush=True)
        dados = coletar_produto(slug, janelas, taxa_usd, hoje)
        destino = DATA_DIR / f"{slug}.json"
        destino.write_text(json.dumps(dados, indent=2, ensure_ascii=False), encoding="utf-8")
        n_err = len(dados["erros"])
        print(f"  OK → {destino}  ({'sem erros' if not n_err else str(n_err)+' erro(s)'})")
        if n_err:
            for e in dados["erros"]:
                print(f"     ! {e}")
        indice.append({"produto": slug, "rotulo": dados["rotulo"], "erros": n_err,
                       "atualizadoEm": dados["atualizadoEm"]})

    (DATA_DIR / "_index.json").write_text(
        json.dumps({"atualizadoEm": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
                    "produtos": indice}, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n✓ FIM · {len(alvos)} produto(s) · índice em {DATA_DIR / '_index.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
