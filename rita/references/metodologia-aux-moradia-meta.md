# Metodologia · Aux Moradia · Meta Ads (cirúrgico)

Arquivo de referência da Rita. Quando rodar o relatório semanal de segunda do Auxílio Moradia, segue esse passo a passo na ordem.

---

## 1 · Mapa de campanhas e contas

### BR (`act_320965166251046`, BRL)

| Campanha | ID | Adsets ativos chave | Otimização | Destino |
|---|---|---|---|---|
| AUXÍLIO MORADIA \| CADASTRO \| QUENTE | `120212210571860439` | 08 SEMELHANTE RD `120214793686570439` · 22 MG TJMG `120246581263370439` | LEAD | Lead Form (SIGN_UP) |
| AUXÍLIO MORADIA \| TRAFEGO SITE \| TOPO \| FRIO | `120233684273740439` | (tráfego topo) | CLICKS | LP |
| AUXÍLIO MORADIA \| WHATSAPP \| FIM \| QUENTE | `120233685006620439` | (todos pausados) | CONVERSATIONS | WhatsApp |

**Lead Form ativo:** `628436196234057` (Auxílio-Moradia | 2025)

### EUA (`act_1271698078245722`, USD)

| Campanha | ID | Adsets | Estado |
|---|---|---|---|
| AUXÍLIO MORADIA \| LEADS \| MENSAGENS \| 17/03/2026 (Original) | `120250269412470112` | 00 LISTAS `120250269412490112` · 01 FORMARAM `120250618232500112` · 02 MG `120253835537240112` | 5 ads WITH_ISSUES desde ban WhatsApp 03/06 · só V4 00 LISTAS rodando |
| AUXÍLIO MORADIA \| LEADS \| MENSAGENS \| 03/06 v2 Tel 8618 (Duplicada) | `120255419353980112` | 00 LISTAS Dup `120255419353970112` · 01 FORMARAM Dup `120255419728880112` · 02 MG Dup `120255419852420112` | Viva, criada após ban como contingência |

**WhatsApp destino EUA:** (11) 97716-8618 (era do Livre IR, agora padrão da Página Silva Pimenta).

---

## 2 · Comandos pra puxar dados

### Insights por nível (substituir CAMP_ID e PERIODO)

```bash
# Campanhas Aux Moradia BR
python .claude/skills/meta-ads-ratos/scripts/insights.py campaign \
  --id 120212210571860439 \
  --since 2026-XX-XX --until 2026-XX-XX \
  --fields spend,impressions,clicks,ctr,cpc,cpm,frequency,actions,cost_per_action_type

# Adsets de uma campanha
python .claude/skills/meta-ads-ratos/scripts/insights.py adset \
  --campaign-id 120212210571860439 \
  --since ... --until ...

# Ads (granular, com rankings)
python .claude/skills/meta-ads-ratos/scripts/insights.py ad \
  --campaign-id 120212210571860439 \
  --since ... --until ... \
  --fields spend,impressions,clicks,ctr,frequency,actions,cost_per_action_type,quality_ranking,engagement_rate_ranking,conversion_rate_ranking
```

### EUA precisa do token EUA

```powershell
$env:META_ADS_TOKEN=<META_ADS_TOKEN_EUA>; python ... --account act_1271698078245722
```

### Janelas obrigatórias
- **30 dias** (tendência longa)
- **14 dias** (ciclo quinzenal)
- **7 dias** (semana atual)

Sempre compara 7 com 14 e 14 com 30 pra ver se a tendência é melhora ou piora.

---

## 3 · Ações na API (todas em PAUSED, com confirmação)

### Pausar ad
```bash
python .claude/skills/meta-ads-ratos/scripts/update.py ad --id <AD_ID> --status PAUSED
```

### Ajustar budget
```bash
python .claude/skills/meta-ads-ratos/scripts/update.py adset --id <ADSET_ID> --daily-budget <CENTAVOS>
```

> ⚠️ Budget em **CENTAVOS** (R$ 43,20 = 4320). Memória `feedback-meta-api-seguranca`.

### Subir ad novo (criativo já criado)
```bash
python .claude/skills/meta-ads-ratos/scripts/create.py ad \
  --adset-id <ADSET_ID> \
  --creative-id <CREATIVE_ID> \
  --name "..." --status PAUSED
```

### Regra de ouro
- Sempre `--status PAUSED` na criação
- Rodar `--validate-only` antes em operações sensíveis
- Nunca DELETAR (pausar ou arquivar)
- Confirmar com William ANTES de mudança real

---

## 4 · Régua de classificação do Aux Moradia

CPL real do produto = **R$ 76** (memória `cpl-aux-moradia`).

| Faixa CPL | Classificação | Cor visual |
|---|---|---|
| ≤ R$ 35 | EXCELENTE (atingiu meta aspiracional) | verde |
| R$ 36 a R$ 76 | SAUDÁVEL (dentro do histórico) | verde |
| R$ 77 a R$ 110 | ATENÇÃO (acima histórico) | amarelo |
| > R$ 110 | CRÍTICO | vermelho |

**EUA em USD:** converter pelo câmbio (~5,20) antes de aplicar a régua.

---

## 5 · Indicadores de fadiga (combinar os 3)

Um ad só é "fadiga confirmada" quando 2 dos 3 disparam:

| Indicador | Sinal de alerta | Sinal crítico |
|---|---|---|
| `frequency` (Meta) | > 3,0 em prospecção | > 5,0 |
| `quality_ranking` | BELOW_AVERAGE_55 | BELOW_AVERAGE_35 |
| `conversion_rate_ranking` | BELOW_AVERAGE_55 | BELOW_AVERAGE_35 |
| CPA do ad em 7d vs 14d | +30% piora | +60% ou mais |

**Ação por nível:**
- 1 disparado → monitorar, ainda dá pra extrair valor
- 2 disparados → planejar troca, ativar `/criativo`
- 3 disparados ou CPA dobrou → propor pausa imediata

---

## 6 · WITH_ISSUES (ads rejeitados Meta)

Detectar via `effective_status == 'WITH_ISSUES'` em `read.py ads`.

**Causa comum no Aux Moradia (jun/2026):** ban WhatsApp do (11) 97716-7482 → ads com `WHATSAPP_MESSAGE` rejeitados em massa (subcode 2923003).

**3 caminhos pra recuperar:**
- **A.** Duplicar o ad dentro do mesmo adset (botão Duplicar UI). Cria gêmeo limpo, mantém learning do adset.
- **B.** Desligar adset, focar no gêmeo Duplicada (se existir).
- **C.** Solicitar análise na UI (Meta reavalia em 24-48h, pode rejeitar de novo).

**Sempre listar no relatório** com motivo + opção recomendada.

---

## 7 · Canibalização (Original vs Duplicada EUA)

Cenário comum desde 03/06/2026: 2 campanhas EUA paralelas (Original + Duplicada) usam **mesmas custom audiences, mesmos criativos, mesma Página**.

**Como detectar:**
- Mesmas Listas em adsets das 2 campanhas
- Soma de budgets diários dos pares
- Comparar CPA do mesmo adset nas 2

**Como resolver:**
- Tabular CPA adset-a-adset (Original 00 LISTAS vs Duplicada 00 LISTAS, etc)
- Manter o melhor de cada par, pausar o pior
- Resultado: 3 adsets vivos (1 de cada campanha · acaba canibalização)

**Cuidado:** se Original tem WITH_ISSUES e Duplicada está rodando, a canibalização é falsa (não está acontecendo de fato). Só apontar canibalização quando os 2 estão ativos e entregando.

---

## 8 · Sazonalidade do Aux Moradia

Eventos que impactam o produto:

| Evento | Período | Impacto |
|---|---|---|
| Posse R1 (residentes médicos) | Fevereiro e Março | Pico de busca por auxílio retroativo |
| Prova residência médica | Outubro a Janeiro | Pico de busca FIES, queda Aux Moradia |
| Dia dos Namorados | 10-12/06 | CPMs +10-15% no Meta |
| Dia dos Pais | 2º domingo de Agosto | CPMs +10-15% |
| Dia das Crianças | 12/10 | CPMs +10-15% |
| Black Friday | última semana Novembro | CPMs +30-50% |
| Decreto presidencial 12.681/2025 | Outubro 2025 | Reduziu de 30% pra 10% o auxílio em curso. Retroativo de período anterior continua 30%. |

**Sempre listar no relatório se o período abrange algum evento.**

---

## 9 · Audit log format (estilo terminal)

Salvar no rodapé do HTML:

```
DD/MM HH:MM PLATAFORMA AÇÃO       | DETALHE | STATUS
15/06 09:00 META-BR    ANALISE    | Ciclo 7 · 7d (09-15/06) · Aux Moradia
15/06 09:05 META-BR    DIAGNOSTICO| CADASTRO QUENTE · CPL R$ 39,39 · SAUDAVEL
15/06 09:10 META-US    DIAGNOSTICO| Duplicada · CPA dobrou · DETERIORANDO

15/06 propor META-BR PAUSAR_AD    | V4 entre 22-26 (08 SR) · CPA R$ 99 · aguardando ok
15/06 propor META-BR ESCALAR      | 08 SR R$ 364,40 → R$ 437,28/dia (+20%) · aguardando ok

15/06 manual META-US DECIDIR      | Original 01 FORMARAM + 02 MG · opção A/B/C
15/06 manual CRM     CRUZAR       | 6 leads 22 MG TJMG no Pipedrive
```

Cores no HTML: timestamp azul, OK verde, WARN amarelo, CRIT vermelho.

---

## 10 · Tracking validation (Passo 4.5 do /otimizar)

Checklist BR:
- [ ] Pixel + evento `Lead` disparando no envio do form (não no clique)
- [ ] CAPI server-side ativo com deduplicação `event_id`
- [ ] Domínio verificado em Events Manager
- [ ] AEM 8 eventos priorizados, `Lead` no top 3
- [ ] Match Quality Score > 6

Checklist EUA:
- [ ] Mesmo do BR, mas evento principal é `Messaging Started`
- [ ] Página com número WhatsApp correto (atualmente 8618)
- [ ] CTA `WHATSAPP_MESSAGE` resolve pelo número padrão da Página

Memória relacionada: o V2 Comente Auxílio depende de bot ManyChat respondendo "auxílio" nos comentários. Sem bot, o CTA cai no vazio.

---

## 11 · Compliance OAB · checklist por copy

Em toda copy nova proposta no relatório, listar:

- [ ] Não promete resultado garantido ("podem", "tem direito" sim · "vai receber" não)
- [ ] Sem linguagem mercantilista ("desconto", "oferta", "última chance" no CTA mercantil)
- [ ] Sem denigrir colegas
- [ ] Tom informativo direito previsto em lei
- [ ] Números factuais verificáveis (R$ 4.106 bolsa SUS R1, +500 médicos defendidos)
- [ ] Flag se houver risco aceito (ex: V2 Lula + 30/10%)

Memória relacionada: `feedback_oab_silva_pimenta` exige flag em TODA copy, mesmo as decididamente mantidas.

---

## 12 · Estrutura de pasta de entrega

```
clientes/silva-pimenta/marketing/trafego-pago/otimizacoes/auxilio-moradia/
├── 2026-MM-DD/
│   ├── INDEX.html                   ← navegação (cards Google + Meta + tracking)
│   └── analises/
│       ├── 01-google-ads.html       ← relatório Google (cliente)
│       └── 02-meta-ads.html         ← relatório Meta (Rita) ← gerado aqui
```

Memória relacionada: `feedback_estrutura_pastas_otimizacao` exige essa estrutura. `feedback_propostas_relatorios_historico` proíbe regerar pastas antigas.

---

## 13 · Lista do que cada ciclo precisa puxar

**Mínimo de chamadas API por ciclo Aux Moradia (7d + 14d + 30d):**

| Conta | Campanha | Nível | Janela |
|---|---|---|---|
| BR | CADASTRO QUENTE | campaign | 7d, 14d, 30d |
| BR | CADASTRO QUENTE | adset | 7d, 14d |
| BR | CADASTRO QUENTE | ad | 7d (com rankings) |
| BR | (outras 2 BR se ativas) | campaign | 7d |
| EUA | Original | campaign | 7d, 14d, 30d |
| EUA | Original | adset | 7d, 14d |
| EUA | Original | ad | 7d (com rankings) |
| EUA | Duplicada | campaign | 7d, 14d |
| EUA | Duplicada | adset | 7d, 14d |
| EUA | Duplicada | ad | 7d (com rankings) |
| BR e EUA | ads com WITH_ISSUES | ad | listar |

**Estimativa:** ~25 chamadas API + 1 read de tracking. Roda em ~3 minutos.

---

## 14 · Comparação histórica (mínimo 3 ciclos)

Tabela obrigatória no relatório com:

| Métrica | C(N-3) | C(N-2) | C(N-1) | C(N atual) |
|---|---|---|---|---|
| BR CPL CADASTRO QUENTE | ... | ... | ... | atual com pill colorida |
| BR leads/dia | ... | ... | ... | ... |
| EUA CPA combinado | ... | ... | ... | ... |
| Adsets com fadiga | ... | ... | ... | ... |
| Ads WITH_ISSUES | ... | ... | ... | ... |

Sempre 1 parágrafo de "narrativa" explicando a tendência (não só números).

---

## 15 · Próximo ciclo (always declarar)

Final do relatório:

```
Próximo ciclo: DD/MM/2026 (segunda)
Foco: [2 ou 3 itens]
Pré-requisito: [o que William precisa decidir antes]
```

Sem isso o ciclo não fecha. Sem foco declarado, próxima Rita não sabe o que validar.
