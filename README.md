# Dashboard de Orçamento — Silva Pimenta + Magalhães Gomes

Painel online de gasto diário por produto com divisão Meta/Google, alertas de estouro/folga, projeção até o fim do mês e comparativo com o mês anterior.

URL pública (depois do deploy): `https://<seu-github>.github.io/gestao-trafego-sp-x9k4/`

## Como funciona

```
GitHub Actions (cron */30 min)
    ↓ roda scripts/coletar.py
    ↓ chama Google Ads, Meta Ads, Pipedrive, PTAX
    ↓ gera data/data.json
    ↓ commit no repo
GitHub Pages serve o frontend
    ↓ index.html lê data/data.json a cada 5 min
TV / sócios olham
```

## Arquivos do repo

```
.
├── index.html, styles.css, script.js   ← frontend
├── logo.png, keepalive.mp4
├── data/
│   ├── data.json                       ← mês corrente (gerado pelo cron)
│   └── data-fechamento-YYYY-MM.json    ← histórico de fechamentos
├── scripts/
│   ├── coletar.py                      ← orquestra Google + Meta + Pipedrive + PTAX
│   ├── google_ads.py                   ← módulo Google Ads
│   ├── meta_ads.py                     ← módulo Meta Ads (3 BMs)
│   ├── pipedrive.py                    ← módulo Pipedrive (leads + ganhos)
│   ├── ptax.py                         ← cotação USD via BCB
│   └── compara-pipedrive.py            ← debug: soma CSV exportado vs API
├── .github/workflows/atualizar.yml     ← cron 30min
├── requirements.txt
└── README.md
```

## Orçamento (fonte: `_contexto/orcamento.md`)

Total mensal **R$ 92.120,66** (sem Livre IR encerrado em 26/mai/2026).

Alterar no `script.js` no array `PRODUTOS` quando mudar orçamento.

## Como ler o card de cada produto

3 métricas diárias (passe o mouse pra ver o tooltip):

| Métrica | Significado | Fórmula |
|---------|-------------|---------|
| **Gastando** | Quanto está gastando por dia hoje (média do mês até agora) | gasto ÷ dias passados |
| **Pode** | Ritmo MÁXIMO permitido/dia até fim do mês pra fechar exatamente no orçamento | (orçamento − gasto) ÷ dias restantes |
| **Pode + / Cortar** | Ajuste REAL: quanto AUMENTAR (verde) ou CORTAR (vermelho) por dia | Pode − Gastando |

**Atenção:** "Pode" NÃO é o quanto pode aumentar. Pra ajustar budget de campanha, sempre olhar **"Pode +"** (verde) ou **"Cortar"** (amarelo/vermelho).

## Lógica de cores

- 🟢 **OK** — consumo ≤ ritmo do mês +5pp
- 🟡 **Atenção** — entre +5pp e +15pp acima do ritmo
- 🔴 **Alerta** — acima de +15pp do ritmo OU > 100% do orçamento

## Deploy passo a passo

### 1. Criar repo no GitHub

```
1. github.com → New repository
2. Nome: gestao-trafego-sp-x9k4 (slug obscuro = "secreto")
3. Visibilidade: Public (necessário pra GitHub Pages grátis)
4. Não criar README (vai vir do push)
```

### 2. Push deste código

Da raiz desta pasta:

```bash
git init
git branch -M main
git add .
git commit -m "init: dashboard online"
git remote add origin https://github.com/<seu-user>/gestao-trafego-sp-x9k4.git
git push -u origin main
```

### 3. Adicionar Secrets no GitHub

`Settings → Secrets and variables → Actions → New repository secret`

Adicionar os 9 segredos (pegar valores do `.claude/skills/google-ads-ratos/.env`, `.claude/skills/meta-ads-ratos/.env`, `.env` raiz):

| Secret | Fonte |
|--------|-------|
| `GOOGLE_ADS_DEVELOPER_TOKEN` | `google-ads-ratos/.env` |
| `GOOGLE_ADS_CLIENT_ID` | `google-ads-ratos/.env` |
| `GOOGLE_ADS_CLIENT_SECRET` | `google-ads-ratos/.env` |
| `GOOGLE_ADS_REFRESH_TOKEN` | `google-ads-ratos/.env` |
| `GOOGLE_ADS_LOGIN_CUSTOMER_ID` | `google-ads-ratos/.env` |
| `META_ADS_TOKEN` | `meta-ads-ratos/.env` |
| `META_ADS_TOKEN_EUA` | `meta-ads-ratos/.env` |
| `META_ADS_TOKEN_LIVRE_IR` | `meta-ads-ratos/.env` |
| `PIPEDRIVE_TOKEN` | `.env` raiz |

### 4. Habilitar GitHub Pages

`Settings → Pages → Source: Deploy from a branch → Branch: main / (root) → Save`

Em ~30s a URL fica disponível em `https://<seu-user>.github.io/gestao-trafego-sp-x9k4/`.

### 5. Rodar o cron a primeira vez

`Actions → Atualizar dashboard → Run workflow → Run` (ou aguardar próximo gatilho do cron).

Depois disso, atualização automática a cada 30 minutos.

## Como rodar/testar localmente

```bash
# 1. Coleta dados (precisa das envs setadas)
export PYTHONIOENCODING=utf-8
export PIPEDRIVE_TOKEN=...
export GOOGLE_ADS_DEVELOPER_TOKEN=...  # e os outros 4
export META_ADS_TOKEN=...
export META_ADS_TOKEN_EUA=...
export META_ADS_TOKEN_LIVRE_IR=...
python scripts/coletar.py

# 2. Sobe servidor estático
python -m http.server 8766

# 3. Abre http://localhost:8766
```

Pra coletar mês fechado (gera `data/data-fechamento-YYYY-MM.json`):

```bash
python scripts/coletar.py --mes 2026-05
```

## Testes

`teste-frontend.js` valida com Playwright que o frontend carrega sem erros, renderiza os 9 cards, badges de comparação, toggle de mês.

```bash
node teste-frontend.js
```

## Manutenção

| Mudança | Onde tocar |
|---------|-----------|
| Orçamento de um produto | `script.js` → array `PRODUTOS` |
| Adicionar produto novo | `script.js` (PRODUTOS) + `scripts/coletar.py` (lista produtos) + `scripts/meta_ads.py` (mapeamento) |
| Trocar cor / layout | `styles.css` (vars `--gold`, `--teal-deep`, etc.) |
| Cadência do cron | `.github/workflows/atualizar.yml` linha `cron:` |

## Histórico

- **2026-06-02** — Online (GitHub Pages + Actions). Antes: HTML local com data-mock.json manual.
- **2026-05-26** — Livre IR encerrado (orçamento R$ 15K saiu do total mensal).
- **2026-05-14** — V1 local com 9 produtos mapeados.
