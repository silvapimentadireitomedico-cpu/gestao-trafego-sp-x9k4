"""Entrega da Rita — manda o aviso das 8h pro William (Discord + WhatsApp).

Primitiva de entrega REUSADA da automação da planilha (rodar_automatico.py,
funções discord()/whatsapp() já testadas). Aqui lê as chaves de os.environ
(secrets na Action; .env local no teste). Não tem token de ads, só webhook
do Discord e apikey do CallMeBot (baixo risco).

Chaves (env / secrets):
  DISCORD_WEBHOOK_AUTOMACOES
  WHATSAPP_CALLMEBOT_PHONE
  WHATSAPP_CALLMEBOT_APIKEY

Uso programático:
  from notificar_rita import notificar
  notificar("Relatório de FIES pronto", link="https://.../relatorios/2026-06-19-fies.html")

Uso CLI (teste):
  python scripts/notificar_rita.py "texto" "https://link-opcional"
"""
import os
import sys
import urllib.parse
import urllib.request


def _discord(texto: str) -> bool:
    url = os.environ.get("DISCORD_WEBHOOK_AUTOMACOES")
    if not url:
        print("[discord] DISCORD_WEBHOOK_AUTOMACOES ausente — pulando")
        return False
    import json
    body = json.dumps({"content": texto[:1990]}).encode("utf-8")
    req = urllib.request.Request(url, data=body,
                                 headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"})
    try:
        urllib.request.urlopen(req, timeout=30).read()
        print("[discord] enviado")
        return True
    except Exception as e:
        print(f"[discord] FALHOU: {e}")
        return False


def _whatsapp(texto: str) -> bool:
    fone = os.environ.get("WHATSAPP_CALLMEBOT_PHONE")
    key = os.environ.get("WHATSAPP_CALLMEBOT_APIKEY")
    if not (fone and key):
        print("[whatsapp] CallMeBot ausente — pulando")
        return False
    txt = texto.replace("**", "*").replace("```", "").strip()
    url = ("https://api.callmebot.com/whatsapp.php?phone=" + fone +
           "&apikey=" + key + "&text=" + urllib.parse.quote(txt[:1500]))
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        urllib.request.urlopen(req, timeout=40).read()
        print("[whatsapp] enviado (CallMeBot)")
        return True
    except Exception as e:
        print(f"[whatsapp] FALHOU: {e}")
        return False


def notificar(texto: str, link: str | None = None) -> dict:
    """Manda o mesmo texto pro Discord e pro WhatsApp. Anexa o link se houver."""
    msg = texto if not link else f"{texto}\n{link}"
    return {"discord": _discord(msg), "whatsapp": _whatsapp(msg)}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Uso: python scripts/notificar_rita.py "texto" ["link"]')
        sys.exit(1)
    texto = sys.argv[1]
    link = sys.argv[2] if len(sys.argv) > 2 else None
    r = notificar(texto, link)
    sys.exit(0 if any(r.values()) else 1)
