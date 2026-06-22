"""Fase 3 — gera o relatório HTML da Rita a partir do JSON dumpado (Action + API Anthropic).

A Rita aqui é READ-ONLY: a única fonte é data/rita/<produto>.json (a Action já coletou).
Este script NÃO toca a API de ads; só chama a API da Anthropic com o JSON + a skill
rita-relatorios (portada em rita/) e devolve o HTML do relatório.

Modelo: claude-opus-4-8 (análise de sócio sênior). Adaptive thinking + streaming
(HTML longo) + prompt caching no prefixo estável (skill + reference do produto).

Cadência (BRT): seg Aux Moradia · ter FIES · qua Seguro · qui Direito Médico.

Uso:
  python scripts/gerar_relatorio_rita.py aux-moradia        # produto explícito
  python scripts/gerar_relatorio_rita.py --auto             # produto do dia (weekday BRT); sem cadência → no-op
  python scripts/gerar_relatorio_rita.py aux-moradia --dry-run   # monta o prompt e mostra tamanhos, SEM chamar a API (testável sem chave)

Saída:
  relatorios/rita-<produto>-YYYY-MM-DD.html   (datado = histórico, não sobrescreve)
  imprime na última linha:  RESUMO::<uma linha pro WhatsApp/Discord>::<caminho>
"""
import argparse
import os
import re
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data" / "rita"
RITA_DIR = ROOT / "rita"
OUT_DIR = ROOT / "relatorios"
BRT = timezone(timedelta(hours=-3))

MODEL = os.environ.get("RITA_MODEL", "claude-opus-4-8")
MAX_TOKENS = int(os.environ.get("RITA_MAX_TOKENS", "32000"))

# produto → (rótulo, arquivo(s) de reference em rita/references/)
PRODUTOS = {
    "aux-moradia": ("Auxílio Moradia", ["auxilio-moradia.md", "metodologia-aux-moradia-meta.md"]),
    "fies": ("FIES", ["fies.md"]),
    "seguro": ("Seguro (Magalhães Gomes)", ["seguro.md"]),
    "direito-medico": ("Direito Médico", ["direito-medico.md"]),
}

# weekday() BRT → produto da cadência (0=seg)
CADENCIA = {0: "aux-moradia", 1: "fies", 2: "seguro", 3: "direito-medico"}

ADAPTER = """Você é a RITA rodando NA NUVEM, em modo de entrega automática diária.

CONTEXTO DE EXECUÇÃO (importante, sobrepõe a skill onde conflitar):
- Você é 100% READ-ONLY. NÃO existe API de ads aqui: a coleta JÁ FOI FEITA por outro
  processo e te entrego os dados PRONTOS num JSON (na mensagem do usuário). NÃO tente
  chamar read.py, insights.py, nem nenhuma API. Todo número que você usar tem que vir
  desse JSON (verificação em cadeia já satisfeita na coleta).
- Leia o campo `_leia_me` do JSON: ele explica a semântica (cohort do Pipedrive por
  add_time, perdas_por_motivo = seção 5.1, gates Google/Meta, rankings UNKNOWN, e as
  2 lacunas v1 que você DEVE reportar como pendência: quebra por "número da campanha"
  e checagem de WhatsApp vivo na LP).
- As janelas 30/14/7d já estão no JSON (campo janelas/janelas_def, com o período exato).
  Declare a janela exata, narre a tendência 30→14→7, compare os ciclos.
- Sazonalidade é conhecimento seu (feriados, Dia dos Pais, prova de residência): aplique
  pelo período do JSON.

ENTREGÁVEIS CIRÚRGICOS OBRIGATÓRIOS (cravar em TABELA própria, NÃO diluir no diagnóstico):
Para o lado GOOGLE de cada produto, sempre que houver dados, inclua estas 3 tabelas de AÇÃO,
cada linha com o MOTIVO explícito:
1. PALAVRAS-CHAVE: por keyword (texto + match), ação = manter / ajustar lance / pausar /
   negativar, com motivo. Quality Score < 4 em DESTAQUE vermelho (gate crítico). Nunca propor
   pausar/negativar a keyword-âncora do produto (ex: "auxilio moradia medico" é intocada;
   no FIES "adimplência/em dia/desconto fies" é REQUISITO, não filtro).
2. TERMOS DE PESQUISA: por termo, ação = VIRAR KEYWORD NOVA (termo que converte e ainda não é
   keyword) / NEGATIVAR (gasto sem conversão e off-persona) / manter, com motivo classificando
   LIXO=público errado (targeting) vs desempenho. NUNCA negativar cidade (atuação nacional) nem
   termo direto do produto. Liste os termos de maior gasto primeiro.
3. QUALIDADE DOS ANÚNCIOS: Google = status de aprovação (APPROVED/WITH_ISSUES/DISAPPROVED) + QS;
   Meta = quality_ranking, conversion_rate_ranking e frequência (freq alta + ranking BELOW =
   fadiga). Ação por anúncio (manter / revisar criativo / pausar) com motivo. Rankings UNKNOWN
   (campanha de mensagem/CTWA ou volume baixo) = não dar veredito, só sinalizar.
Se um bloco não tiver dado suficiente, diga "imaturo/sem dado" em vez de inventar. Cada tabela
fecha com 1 linha de "ação recomendada hoje" amarrada ao Plano 3 camadas.

SAÍDA (obrigatório):
- Responda APENAS com o documento HTML completo do relatório (de <!DOCTYPE html> até
  </html>), seguindo a estrutura de 17 seções e a paleta do template
  (rita/references/template-html-meta.md). Sem ```html, sem comentário antes ou depois,
  sem preâmbulo. O primeiro caractere da resposta é "<".
- Zero travessões (regra inviolável do William): use vírgula, dois pontos, ponto,
  parênteses ou reescrita.
- Onde a skill mandar "salvar HTML / atualizar INDEX / audit log", inclua o conteúdo
  correspondente DENTRO do próprio HTML (você não tem filesystem aqui).
"""


def _read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def _produto_do_dia() -> str | None:
    return CADENCIA.get(datetime.now(BRT).weekday())


def montar_prompt(slug: str) -> tuple[list, str, dict]:
    rotulo, refs = PRODUTOS[slug]
    skill = _read(RITA_DIR / "SKILL.md")
    template = _read(RITA_DIR / "references" / "template-html-meta.md")
    refs_txt = "\n\n".join(
        f"===== rita/references/{r} =====\n{_read(RITA_DIR / 'references' / r)}" for r in refs
    )
    dados = _read(DATA_DIR / f"{slug}.json")

    # system = prefixo ESTÁVEL (adapter + skill + template + reference do produto) → cacheável.
    sistema_txt = (
        ADAPTER
        + "\n\n========== SKILL rita-relatorios ==========\n" + skill
        + "\n\n========== TEMPLATE HTML ==========\n" + template
        + f"\n\n========== PLAYBOOK DO PRODUTO ({rotulo}) ==========\n" + refs_txt
    )
    system = [{"type": "text", "text": sistema_txt, "cache_control": {"type": "ephemeral"}}]

    hoje = datetime.now(BRT).date().isoformat()
    user = (
        f"Gere o relatório da Rita do produto {rotulo} (slug {slug}) para hoje, {hoje}.\n"
        "Os dados coletados (única fonte) estão no JSON abaixo. Siga o critério de sucesso "
        "da skill, item por item, antes de fechar.\n\n"
        f"```json\n{dados}\n```"
    )
    tam = {"system_chars": len(sistema_txt), "json_chars": len(dados), "refs": refs}
    return system, user, tam


def _limpar_html(txt: str) -> str:
    t = txt.strip()
    if t.startswith("```"):
        t = re.sub(r"^```[a-zA-Z]*\n", "", t)
        t = re.sub(r"\n```\s*$", "", t)
    i = t.find("<!DOCTYPE")
    if i == -1:
        i = t.find("<html")
    return (t[i:] if i > 0 else t).strip()


def gerar(slug: str, dry_run: bool) -> int:
    if slug not in PRODUTOS:
        print(f"ERRO: produto '{slug}' inválido. Válidos: {list(PRODUTOS)}")
        return 2
    if not (DATA_DIR / f"{slug}.json").exists():
        print(f"ERRO: {DATA_DIR / (slug + '.json')} não existe. Rode o rita_collector antes.")
        return 3

    system, user, tam = montar_prompt(slug)
    aprox_tok = (tam["system_chars"] + tam["json_chars"]) // 4
    print(f"[{slug}] system {tam['system_chars']:,} chars · json {tam['json_chars']:,} chars "
          f"· refs {tam['refs']} · ~{aprox_tok:,} tokens de input (estimativa /4)")

    if dry_run:
        print("DRY-RUN: prompt montado OK, API não chamada. Primeiras linhas do user:")
        print("  " + user.splitlines()[0])
        print(f"  (system começa com: {system[0]['text'][:60]!r})")
        return 0

    try:
        import anthropic
    except ImportError:
        print("ERRO: pacote 'anthropic' não instalado (pip install -r requirements-rita.txt)")
        return 4
    if not (os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_AUTH_TOKEN")):
        print("ERRO: ANTHROPIC_API_KEY ausente no ambiente (secret no GitHub Actions).")
        return 5

    client = anthropic.Anthropic()
    print(f"[{slug}] chamando {MODEL} (adaptive thinking, streaming, max_tokens {MAX_TOKENS})...")
    with client.messages.stream(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        thinking={"type": "adaptive"},
        output_config={"effort": "high"},
        system=system,
        messages=[{"role": "user", "content": user}],
    ) as stream:
        msg = stream.get_final_message()

    if msg.stop_reason == "refusal":
        print(f"ERRO: resposta recusada (refusal): {getattr(msg, 'stop_details', None)}")
        return 6
    html = _limpar_html("".join(b.text for b in msg.content if b.type == "text"))
    if "<html" not in html.lower():
        print("ERRO: resposta não parece HTML. Início:\n" + html[:300])
        return 7

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    hoje = datetime.now(BRT).date().isoformat()
    destino = OUT_DIR / f"rita-{slug}-{hoje}.html"
    destino.write_text(html, encoding="utf-8")

    u = msg.usage
    rel = destino.relative_to(ROOT).as_posix()
    print(f"[{slug}] OK → {rel}  ({len(html):,} chars · in {u.input_tokens} "
          f"+cache_read {getattr(u, 'cache_read_input_tokens', 0)} · out {u.output_tokens} tok)")
    rotulo = PRODUTOS[slug][0]
    resumo = f"🤖 Rita: relatório de *{rotulo}* de {hoje} pronto."
    print(f"RESUMO::{resumo}::{rel}")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("produto", nargs="?", help="slug (aux-moradia, fies, seguro, direito-medico)")
    ap.add_argument("--auto", action="store_true", help="usa o produto da cadência do dia (BRT)")
    ap.add_argument("--dry-run", action="store_true", help="monta o prompt sem chamar a API")
    a = ap.parse_args()

    if a.auto and not a.produto:
        slug = _produto_do_dia()
        if not slug:
            print(f"{datetime.now(BRT).date()}: sem cadência hoje (cadência é seg a qui). Nada a gerar.")
            return 0
        print(f"--auto: cadência do dia = {slug}")
        # Idempotência: com várias tentativas de cron na manhã, só a 1a gera; as outras pulam.
        ja = OUT_DIR / f"rita-{slug}-{datetime.now(BRT).date().isoformat()}.html"
        if ja.exists():
            print(f"--auto: relatório de hoje já existe ({ja.name}); pulando (idempotência, sem renotificar).")
            return 0
    elif a.produto:
        slug = a.produto
    else:
        print("Informe um produto ou use --auto.")
        return 2
    return gerar(slug, a.dry_run)


if __name__ == "__main__":
    sys.exit(main())
