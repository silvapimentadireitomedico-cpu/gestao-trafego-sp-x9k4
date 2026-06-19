# Template HTML · Relatório Meta da Rita

Estrutura, paleta e snippets pra renderizar o HTML do relatório semanal Meta. Referência visual: `clientes/silva-pimenta/marketing/trafego-pago/otimizacoes/auxilio-moradia/2026-06-15/analises/02-meta-ads.html` (Ciclo 7, gerado em 15/06/2026).

---

## 1 · Paleta Silva Pimenta

```css
:root {
  --teal: #1A4758;          /* primária, header gradient */
  --teal-dark: #133544;
  --champagne: #C5A57A;     /* destaque, eyebrows */
  --champagne-dark: #A88958;
  --bege: #f7f5f0;          /* background */
  --texto: #1A1A1A;
  --texto-secundario: #555;
  --verde: #22c55e;         /* success */
  --vermelho: #ef4444;      /* critical */
  --amarelo: #f59e0b;       /* warning */
  --azul: #3b82f6;          /* info */
}
```

## 2 · Fonte

```html
<link href="https://fonts.googleapis.com/css2?family=Jost:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
```

Body: `font-family: 'Jost', sans-serif`.

---

## 3 · 17 seções obrigatórias

### 3.1 Header (gradient teal)
- Eyebrow "Silva Pimenta · Auxílio Moradia · Meta Ads" (champagne uppercase)
- H1 com produto + data + ciclo número
- Subtitle com janela de análise
- 3 badges: BR / EUA Original / EUA Duplicada (ok/warn/crit)

### 3.2 Skills usadas (cards transparência)
3 cards lado a lado:
- meta-ads-ratos (Execução · API): o que puxou
- ads-ratos (Inteligência · Benchmarks): que regras aplicou
- /otimizar (Workflow · Diagnóstico): que passos rodou

### 3.3 Skills não acionadas (alert info)
- Por que `/criativo` não foi chamado
- Por que outras skills foram puladas

### 3.4 Resumo executivo (grid 4 KPIs)
- CPL médio BR (cor por classificação)
- Leads BR (volume + delta)
- CPA EUA (cor por classificação)
- Ads WITH_ISSUES (warn se > 0)

Cada KPI tem `delta` indicando comparação com ciclo anterior (verde se melhorou, vermelho se piorou).

### 3.5 Achados que mudam decisão (3 a 5 alerts coloridos)
Cada achado:
- Ícone + título
- Texto curto explicando o que aconteceu + número
- Texto curto da consequência ou ação

### 3.6 Performance ad-a-ad BR (tabela)
Colunas: Criativo · Adset · Gasto · Conv · CPA Meta · Freq · Q/Conv Rank · Veredito

Linhas coloridas: `row-best` verde, `row-warn` amarelo, `row-bad` vermelho.

Pills no veredito: "Vencedor, escalar" (ok), "Saturando, monitorar" (warn), "Pausar, CPA acima" (crit).

### 3.7 Performance ad-a-ad EUA (tabela)
Mesma estrutura. Adicionar coluna "Campanha · Adset" pra distinguir Original vs Duplicada.

### 3.8 Ads WITH_ISSUES (tabela)
Colunas: Campanha · Adset · Ad · Motivo
Motivo típico: "Rejeitado análise (code 2490468)" ou "Rejeitado pós ban".

### 3.9 Comparação histórica (tabela 3-5 ciclos)
Métricas obrigatórias:
- BR CPL CADASTRO QUENTE (pill colorida no ciclo atual)
- BR leads/dia
- EUA CPA combinado
- EUA 01 FORMARAM CPA
- 22 MG BR CPL

Embaixo: parágrafo "Narrativa" explicando tendência.

### 3.10 Sazonalidade (tabela curta)
- Evento, Janela, Impacto
- Listar só eventos do período do ciclo

### 3.11 Diagnóstico (3 a 4 alerts)
1 alert por gargalo, priorizado:
- Gargalo 1 (alto impacto): vermelho
- Gargalo 2 (médio impacto): amarelo
- Sem gargalo: verde (motor estável)
- Gargalo 4 (médio impacto): vermelho

### 3.12 Plano de ação (3 camadas)
Lista de ações como cards individuais (borda colorida + ícone + título + desc + meta).

- Camada 1 HOJE (vermelho): pausar zumbis, escalar vencedor
- Camada 2 ESTA SEMANA (amarelo): decisões estratégicas, validações Pipedrive
- Camada 3 PRÓXIMAS 2 SEMANAS (azul): testes, briefings, tracking

### 3.13 Validação tracking (tabela com pills)
- Item, Status (pill OK/WARN/CRIT), Observação
- Linhas: Pixel + Lead, messaging_conversation, CAPI, AEM, Match Quality, mecânica V2

### 3.14 Compliance OAB (alert + lista)
- Sem copy nova: "Não aplicável nesse ciclo"
- Com copy: checklist OAB por copy + flag de risco aceito (memória `video-lula-risco-assumido` etc)
- Sempre lembretes ativos das memórias relacionadas

### 3.15 Audit log (estilo terminal)
Background preto `#0f172a`, texto cinza `#94a3b8`, monospace. Timestamps azuis, OK verde, WARN amarelo, CRIT vermelho.

### 3.16 Próximo ciclo (alert info)
Data + foco + pré-requisito.

### 3.17 Footer
Identificação Silva Pimenta + skills usadas + caminho do arquivo.

---

## 4 · Snippet base do <style>

Cola no `<head>`:

```css
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Jost',sans-serif;background:var(--bege);color:var(--texto);line-height:1.6}
.container{max-width:1180px;margin:0 auto;padding:48px 24px}

header{background:linear-gradient(135deg,var(--teal) 0%,var(--teal-dark) 100%);color:#fff;padding:48px 24px}
.eyebrow{font-size:12px;text-transform:uppercase;letter-spacing:2px;color:var(--champagne);font-weight:600;margin-bottom:12px}
h1{font-size:32px;font-weight:700;margin-bottom:8px;line-height:1.15}
.subtitle{font-size:16px;opacity:0.85;margin-top:6px}

.status-badge{display:inline-block;padding:6px 16px;border-radius:20px;font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:1px}
.status-badge.ok{background:var(--verde);color:#fff}
.status-badge.warn{background:var(--amarelo);color:#fff}
.status-badge.crit{background:var(--vermelho);color:#fff}

.section-title{font-size:24px;font-weight:700;color:var(--teal);margin:48px 0 18px;padding-bottom:12px;border-bottom:2px solid var(--champagne)}

.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px;margin-bottom:32px}
.card{background:#fff;border-radius:12px;padding:24px;box-shadow:0 2px 8px rgba(0,0,0,0.06);border-left:4px solid var(--champagne)}

.alert-box{background:#fef2f2;border-left:4px solid var(--vermelho);padding:22px;border-radius:8px;margin-bottom:14px}
.alert-box.warning{background:#fff8e1;border-left-color:var(--amarelo)}
.alert-box.success{background:#f0fdf4;border-left-color:var(--verde)}
.alert-box.info{background:#eff6ff;border-left-color:var(--azul)}
.alert-box h3{font-size:17px;margin-bottom:8px}

.summary-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:32px}
.summary-grid > div{background:#fff;padding:18px;border-radius:8px;text-align:center;border-top:3px solid var(--champagne)}
.summary-grid .num{font-size:26px;font-weight:700;color:var(--teal);display:block;line-height:1.1}
.summary-grid .num.danger{color:var(--vermelho)}
.summary-grid .num.success{color:var(--verde)}
.summary-grid .num.warn{color:var(--amarelo)}
.summary-grid .label{font-size:11px;text-transform:uppercase;letter-spacing:0.5px;color:var(--texto-secundario);margin-top:6px;display:block}
.summary-grid .delta{font-size:11px;color:var(--texto-secundario);margin-top:3px;display:block}
.summary-grid .delta.up{color:var(--verde)}
.summary-grid .delta.down{color:var(--vermelho)}

table{width:100%;border-collapse:collapse;background:#fff;border-radius:8px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.04);margin-bottom:24px;font-size:14px}
th{background:var(--teal);color:#fff;text-align:left;padding:12px 14px;font-weight:600;font-size:13px;text-transform:uppercase;letter-spacing:0.5px}
td{padding:11px 14px;border-bottom:1px solid #f0ebe2;vertical-align:middle}
tr.row-best td{background:#f0fdf4}
tr.row-bad td{background:#fef2f2}
tr.row-warn td{background:#fff8e1}

.pill{display:inline-block;padding:3px 10px;border-radius:12px;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.5px}
.pill.ok{background:#dcfce7;color:#166534}
.pill.warn{background:#fef3c7;color:#92400e}
.pill.crit{background:#fee2e2;color:#991b1b}
.pill.info{background:#dbeafe;color:#1e40af}
.pill.neutral{background:#f1f5f9;color:#475569}

.action-list{list-style:none;padding:0}
.action-list li{background:#fff;padding:16px 20px;margin-bottom:10px;border-radius:8px;border-left:4px solid var(--teal);display:flex;gap:14px;align-items:flex-start}
.action-list li.crit{border-left-color:var(--vermelho)}
.action-list li.warn{border-left-color:var(--amarelo)}
.action-list li.ok{border-left-color:var(--verde)}
.action-list .action-title{font-weight:600;color:var(--teal);margin-bottom:4px}
.action-list .action-desc{font-size:14px;color:var(--texto-secundario)}
.action-list .action-meta{font-size:12px;color:var(--champagne-dark);font-weight:600;margin-top:6px;text-transform:uppercase;letter-spacing:0.5px}

.audit-log{background:#0f172a;color:#94a3b8;font-family:'Courier New',monospace;padding:22px;border-radius:8px;font-size:12px;line-height:1.7;overflow-x:auto}
.audit-log .ts{color:#60a5fa}
.audit-log .ok{color:#34d399}
.audit-log .warn{color:#fbbf24}
.audit-log .crit{color:#f87171}

footer{background:var(--teal-dark);color:#fff;padding:32px 24px;text-align:center;margin-top:60px;font-size:13px;opacity:0.92}

@media (max-width:768px){.summary-grid{grid-template-columns:repeat(2,1fr)}h1{font-size:24px}table{font-size:12px}}
```

---

## 5 · Esqueleto HTML (copia, ajusta os números)

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Aux Moradia · Meta Ads · Ciclo N · YYYY-MM-DD</title>
<link href="https://fonts.googleapis.com/css2?family=Jost:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root { ... cole as variáveis }
... cole o snippet base
</style>
</head>
<body>
<header>
  <div class="container">
    <div class="eyebrow">Silva Pimenta &middot; Auxílio Moradia &middot; Meta Ads</div>
    <h1>Ciclo N &middot; Diagnóstico Semanal &middot; DD/MM/2026</h1>
    <p class="subtitle">Janela 7 dias (DD/MM a DD/MM) &middot; comparação com Ciclos N-1 e N-2</p>
    <div class="status-badges">
      <span class="status-badge ok">BR Saudável (CPL R$ XX)</span>
      <span class="status-badge crit">EUA Duplicada deteriorando</span>
      <span class="status-badge warn">EUA Original quase morta</span>
    </div>
  </div>
</header>

<div class="container">
  <!-- 1. Skills usadas -->
  <h2 class="section-title">1. Skills usadas nesse diagnóstico</h2>
  <div class="cards">
    <div class="card">
      <span class="skill-type">Execução &middot; API</span>
      <h4>meta-ads-ratos</h4>
      <div class="skill-desc">...</div>
    </div>
    <div class="card">...</div>
    <div class="card">...</div>
  </div>

  <!-- 2. Resumo executivo -->
  <h2 class="section-title">2. Resumo executivo &middot; 4 KPIs principais</h2>
  <div class="summary-grid">
    <div>
      <span class="num success">R$ XX</span>
      <span class="label">CPL médio BR</span>
      <span class="delta up">-X% vs Ciclo N-1</span>
    </div>
    <div>...</div>
    <div>...</div>
    <div>...</div>
  </div>

  <!-- ... seguir com seções 3 a 17 ... -->

  <!-- 15. Audit log -->
  <h2 class="section-title">15. Audit log</h2>
  <div class="audit-log">
    <span class="ts">DD/MM HH:MM</span> META-BR ANALISE | Ciclo N &middot; 7d ...
    ...
  </div>
</div>

<footer>
  Silva Pimenta &middot; Auxílio Moradia &middot; Meta Ads &middot; Ciclo N<br>
  Gerado em DD/MM/2026 via skills <code>meta-ads-ratos</code> + <code>ads-ratos</code> + <code>/otimizar</code><br>
  Arquivo: <code>clientes/silva-pimenta/marketing/trafego-pago/otimizacoes/auxilio-moradia/YYYY-MM-DD/analises/02-meta-ads.html</code>
</footer>
</body>
</html>
```

---

## 6 · INDEX.html da pasta da data

Atualizar (ou criar) o `INDEX.html` da pasta `YYYY-MM-DD/` com card pro Meta:

```html
<a href="analises/02-meta-ads.html" class="card">
  <div class="card-icon">📱</div>
  <div class="card-title">Diagnóstico Meta Ads &middot; Ciclo N (semanal)</div>
  <div class="card-desc">
    3 campanhas Aux Moradia. CPL BR R$ XX &middot; EUA Duplicada CPA $ XX &middot; X ads WITH_ISSUES.
    Plano 3 camadas hoje/semana/2sem + skills usadas.
  </div>
</a>
```

---

## 7 · Regras visuais inegociáveis

- **Zero travessões.** Use `&middot;` (·), vírgula, dois pontos, parênteses. Nunca `&mdash;` ou `&ndash;`.
- **Tom Silva Pimenta.** Direto, sem juridiquês, sem mercantilismo.
- **Pills em vez de prosa pra status.** "Vencedor escalar" em pill verde, "Pausar saturou" em pill vermelha.
- **Tabelas têm cor por linha** (`row-best`/`row-warn`/`row-bad`), não só pill no fim.
- **Audit log com timestamps coloridos** azul/verde/amarelo/vermelho.
- **Mobile responsive** (grid 4 → 2 colunas em < 768px).
- **Sem JavaScript.** HTML estático standalone.

---

## 8 · Como referenciar exemplo concreto

Quando precisar de exemplo visual de qualquer seção, abrir:
`clientes/silva-pimenta/marketing/trafego-pago/otimizacoes/auxilio-moradia/2026-06-15/analises/02-meta-ads.html`

Foi o relatório referência usado pra calibrar essa Rita.
