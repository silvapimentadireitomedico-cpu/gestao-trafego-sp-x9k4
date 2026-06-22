# Playbook de Análise — Auxílio Moradia (Silva Pimenta)

> Dossiê de inteligência do produto pra Rita fazer relatório e otimização CIRÚRGICOS.
> Carregar SEMPRE que o produto for Auxílio Moradia (cadência: segunda).
> Destila tudo que foi aprendido em campo até 15/06/2026. Atualizar quando algo mudar.

---

## 1. Identidade do produto

**O que é:** ação judicial pra médico-residente (ativo ou ex, até 5 anos) receber retroativo do auxílio-moradia que o hospital não pagou. Base: Lei 6.932/81 + Decreto 12.681/2025. Valor típico: até R$ 70 mil.

**Avatar:** médico residente 24-32 anos, bolsa baixa. Em geral **não sabe que tem esse direito**.

**Contas:**
| Canal | Conta | Observação |
|---|---|---|
| Google Ads | `3560859574` (356-085-9574) "LP - Auxílio Moradia" | 1 campanha ENABLED: "Pesquisa \| 01 \| BRASIL - AM" |
| Meta BR | (confirmar act_ no CLAUDE.md SP — Cadastro Quente) | onde o produto realmente performa |
| Meta EUA | `act_1271698078245722` (token `META_ADS_TOKEN_EUA`) | médico BR morando nos EUA |

**Números reais auditáveis** (memory `project_silva_pimenta_numeros_aux_moradia`): +5.000 médicos defendidos, 98% aprovação, 256 avaliações Google 5★, +20 anos. **Nunca inflar nem trocar.**

**WhatsApp de campanha:** (11) 97716-**8618** (LPs de tráfego pago desde 03/jun). NÃO usar o 7482 (reserva) nas campanhas.

**Régua de CPL real: R$ 76** (memory `project_silva_pimenta_cpl_aux_moradia`). O R$ 15-35 do benchmarks-br.md é meta aspiracional, **não** régua de diagnóstico.

---

## 2. A TESE ESTRATÉGICA (o aprendizado mais importante)

**Auxílio Moradia é produto de INTERRUPÇÃO, não de busca.**

- O médico não sabe que tem o direito → **quase ninguém pesquisa** isso no Google.
- Sinal de campo (15/06): IS de Search em **97% com só ~45 impressões/dia**. Ou seja, já pegamos quase toda a busca que existe, e ainda assim é pouquíssima. **O teto do mercado de busca é baixíssimo.**
- Meta Ads (interrupção, "você sabia que tem direito a R$ 70 mil?") gera demanda e converte muito melhor: CPL BR ~R$ 39 vs Google ~R$ 812 / ∞.

**Regra de negócio fixa (William, 15/06):** **SEMPRE manter uma campanha ativa no Google Ads** desse produto, mesmo sabendo que o Meta converte melhor. O Search fica no ar por (1) captura de fundo de funil — quem já sabe e procura é lead quente, (2) defesa do nome no leilão, (3) reforço pra quem viu o Meta e depois pesquisa. **Nunca recomendar matar/pausar a campanha Google.** O trabalho é manter EFICIENTE (budget enxuto), não questionar a existência.

**Implicação pro relatório:** não tratar "Google com pouco volume" como falha a ser cortada. Tratar como característica do canal nesse produto. A pergunta certa NÃO é "vale manter?", é "o budget está no tamanho certo pra eficiência?". Budget atual: **R$ 60/dia** (reduzido de R$ 140 em 15/06 — não faz sentido queimar R$ 140 num mercado de 45 buscas/dia).

---

## 3. Setup técnico atual (pra não diagnosticar errado)

**Landing page (v3):** `https://auxilio-moradia.silvapimenta.com.br/`
- Cloudflare Pages (projeto `aux-moradia-sp`), estático e rápido (TTFB <100ms).
- É **subdomínio do silvapimenta.com.br** de propósito (ver armadilha #1).
- Form (9 campos) + botão WhatsApp. Ambos são leads.

**Tracking de conversão (2 conversões, AMBAS biddable desde 15/06):**
| Caminho na LP | Conversão Google Ads | Categoria | Label |
|---|---|---|---|
| Form "análise gratuita" | Envio de Formulário (ID 6700663604) | SUBMIT_LEAD_FORM | `AW-11334960527/THRjCLSGkPsYEI-L95wq` |
| Botão WhatsApp (modal) | Botão do WhatsApp \| AM (ID 6764030780) | CONTACT | `AW-11334960527/bHaVCLzWq5kZEI-L95wq` |

**Fluxo do lead:** LP → `fetch('/api/lead')` (Cloudflare Pages Function) → Pipedrive cria **Person + Lead (label AUXÍLIO MORADIA) + Note + campos custom** (PROFISSÃO, INSTITUIÇÃO, INÍCIO/TÉRMINO RESIDÊNCIA). Em paralelo: Web3Forms (email) + gtag (conversão) + abre WhatsApp 8618.
- Label AUXÍLIO MORADIA no Pipedrive: `68477770-00da-11f0-aacd-39462ebe07ed`.

---

## 4. Metodologia de análise — a ORDEM certa pra ESTE produto

A apostila (7 passos) é a base, mas neste produto **3 checagens vêm ANTES**, porque já mascararam o diagnóstico:

### Passo 0 — A campanha está SERVINDO? (checar SEMPRE primeiro)
```
SELECT ad_group_ad.ad.id, ad_group_ad.status, ad_group_ad.policy_summary.approval_status,
       ad_group_ad.policy_summary.policy_topic_entries, ad_group_ad.ad.final_urls
FROM ad_group_ad WHERE campaign.status='ENABLED' AND ad_group_ad.status='ENABLED'
```
Se `approval_status = DISAPPROVED` → a campanha está MORTA, qualquer outra métrica é ruído. Ver armadilha #1.

### Passo 1 — O tracking está VIVO e apontado pro lugar certo?
```
SELECT campaign_conversion_goal.category, campaign_conversion_goal.origin, campaign_conversion_goal.biddable
FROM campaign_conversion_goal WHERE campaign.id = 23688614764
```
Confirmar que SUBMIT_LEAD_FORM **e** CONTACT estão `biddable=True`. Se o Smart Bidding está otimizando pra uma conversão que a LP não dispara mais → bidding cego (ver armadilha #2).

### Passo 2 — Tem lead REAL? (não confiar só no "conversions" da plataforma)
Cruzar SEMPRE com o Pipedrive. "Conversions"/"leads" no Google e no Meta contam clique/submit/mensagem, mas o lead pode ter abandonado. Fonte da verdade de lead qualificado = Pipedrive.
```bash
curl -s "https://silvapimenta.pipedrive.com/api/v1/leads?api_token=<PIPEDRIVE_TOKEN>&limit=500&archived_status=all" 
# filtrar label 68477770-... e add_time >= início do período
```

**Cruzar os LEADS, não só os deals/tags (instrução William 22/06):** a automação **Tag Lead** (Digisac → Pipedrive) cria um LEAD pra cada contato e grava nele **número da campanha, público, criativo e as respostas do formulário**. Esses campos estão no Lead, não só no deal. Ler os campos custom do Lead pra atribuir cada lead à campanha/adset/criativo de origem. Isso dá um cruzamento muito mais rico que olhar só os deals fechados ou só a tag de qualidade. NÃO depender só da tag de qualidade dos deals (que ainda calibra pós 16/06) — usar a origem gravada no próprio lead.

### Passo 2b — Qualidade do lead (LIXO) só com CERTEZA, nunca por suspeita (regra dura William 22/06)
É **PROIBIDO** apontar um público/criativo como fonte de LIXO por inferência ("público amplo costuma trazer lixo", "suspeito principal: Semelhante RD"). Isso é suspeita, não diagnóstico.
**O método correto:** pegar TODOS os leads/deals marcados como LIXO (e AÇÃO INVIÁVEL) no período → pra CADA um, ler no Pipedrive **de qual campanha + público + criativo veio** (campos gravados pelo Tag Lead) → tabular a origem real → só então concluir quem traz lixo, com número e nome. Sem isso, o relatório diz "qualidade a verificar", não acusa ninguém. A régua "CPL baixo não é qualidade" continua válida, mas a culpa só se atribui com a origem verificada lead a lead.

### Passo 3 — Apostila (7 passos), nesta ordem
1. **Search terms** (`read.py search-terms`) + negativas já aplicadas. Cortar desperdício. (Mas ver regras §6: não negativar cidade nem termo direto do produto.)
2. **Quality Score decomposto** (`read.py quality-scores`): QS≤4 = pagando caro. Cruzar os 3 componentes (anúncio / página / CTR esperado).
3. **Parcela de impressão**: perdida por orçamento vs classificação. Neste produto a IS costuma ser alta (mercado pequeno) — perda por orçamento alta NÃO justifica subir budget se CPL está ruim.
4. **Match types**: sem Ampla. PHRASE/EXACT.
5. **Estratégia de lance**: ver §6.
6. **Anúncios/extensões**: RSAs apontando pro mesmo domínio (armadilha #1); CTR esperado.
7. **Higiene**: Display off, Parceiros de Pesquisa off.

### Passo 4 — Tendência 30 → 14 → 7 + device
Ler a evolução pra separar causa de efeito. Device: historicamente Desktop converte pior aqui (ajuste -30% aplicado em 01/06).

---

## 5. ARMADILHAS conhecidas (checklist anti-erro — cada uma já custou dias)

1. **`ONE_WEBSITE_PER_AD_GROUP`** (memory homônima): todos os RSAs (ENABLED **e** PAUSED) do Ad Group têm que apontar pro MESMO domínio raiz. Trocar Final URL pra outro domínio (ex: `.pages.dev`) reprova o anúncio **silenciosamente** e mata a campanha. Por isso a LP usa subdomínio `auxilio-moradia.silvapimenta.com.br` (mesmo raiz que a home). Se for trocar URL, conferir TODOS os RSAs.

2. **Goal Config apontando pra conversão morta:** quando a LP muda (ex: migração v2→v3), a conversão que ela dispara pode mudar. Se o `campaign_conversion_goal` biddable continuar apontando pra conversão antiga (que não dispara mais), o Smart Bidding fica cego → CPC explode, CTR cai, 0 conversão contabilizada. Sempre validar: **a conversão biddable é a mesma que a LP dispara?**

3. **"Conversions" do Google ≠ leads reais.** Sempre cruzar com Pipedrive. Já teve 2 "Envio de Formulário" no Google e 0 lead no Pipedrive no mesmo período.

4. **`primary_for_goal` é legacy** e não muda nada via API (mutate retorna OK fantasma). O que controla o Smart Bidding é `campaign_conversion_goal.biddable` (via `CampaignConversionGoalService`). Algumas conversions system-managed (GET_DIRECTIONS, YOUTUBE) nem aceitam mutate.

5. **CPC explode (R$ 98 já aconteceu)** quando Maximize Conversions roda sem sinal de conversão biddable. Sintoma de bidding cego — investigar Passo 1.

6. **Orçamento Google Ads é em MICROS** (R$ 60 = 60.000.000 micros). Diferente do Meta (centavos).

7. **Higiene de inventário Meta (limpeza de WITH_ISSUES/DISAPPROVED/PAUSED) — regra William 22/06:** pode limpar anúncios mortos pra desentupir o gerenciador, MAS com 2 travas: (a) **só ARQUIVAR, nunca deletar** (memory `feedback_meta_api_seguranca`); (b) **só os que comprovadamente NÃO gastam verba há +2 semanas** — verificar o `spend` dos últimos 14d de CADA ad antes de arquivar (`insights account --level ad --date-preset last_14d`), nunca arquivar cego pelo status. **NÃO arquivar criativo recém-subido que está WITH_ISSUES/DISAPPROVED temporário durante revisão do Meta** (ex: criativo novo do dia). DISAPPROVED que está servindo (configured ACTIVE) → pausar e mandar revisar o criativo, não arquivar. Canibalização (mesma campanha duplicada rodando os mesmos adsets) se resolve mantendo o melhor de cada par e pausando o pior, não arquivando.

---

## 6. Regras de negócio fixas (não violar)

- **Sempre manter campanha Google ativa** (§2). Nunca propor pausar/matar.
- **Otimizar por QUALIDADE, não por CPL isolado** (memory `feedback_otimizacao_por_qualidade_nao_cpl`): decidir por vendas + tags Pipedrive. Não pausar campanha cara que traz lead qualificado; cortar só o que traz lixo.
- **Termo direto do produto não pausa nem negativa** ("Auxílio Moradia Médico" é keyword-âncora intocada). Corrige via LP + RSA + QS.
- **Nunca negativar cidades** — atuação nacional.
- **OAB:** flaggar sempre nas copies/RSAs (ex: "98% de aprovação", "+5.000 médicos" são reais e auditáveis, risco assumido conscientemente pelo William). Flag, não impõe pausa.
- **Sem travessões** em nenhum texto.
- **Lance atual:** Maximize Conversions (decisão 15/06 — manter, agora que tem 2 sinais biddable). Reavaliar pra Max Cliques c/ teto só se continuar sem volume após teste justo.

---

## 7. Comandos de API prontos (copy-paste)

```bash
# Detectar Python: rodar da raiz do workspace
CID=3560859574

# Métricas da campanha (rodar pra LAST_30_DAYS, LAST_14_DAYS, LAST_7_DAYS)
python .claude/skills/google-ads-ratos/scripts/read.py campaigns --customer-id $CID

# Search terms (desperdício)
python .claude/skills/google-ads-ratos/scripts/read.py search-terms --customer-id $CID

# Quality Score decomposto
python .claude/skills/google-ads-ratos/scripts/read.py quality-scores --customer-id $CID

# Insights device/hora/dia
python .claude/skills/google-ads-ratos/scripts/insights.py account --customer-id $CID --date-range LAST_7_DAYS
```

Queries GAQL custom (via `lib.run_query`) pra o que o read.py não cobre: status de aprovação do anúncio (Passo 0), `campaign_conversion_goal` biddable (Passo 1), `conversion_action` + tag_snippets (achar label), histórico diário (`segments.date`), device (`segments.device`). Nota: `LAST_2_DAYS` não existe no GAQL — usar datas absolutas ou `LAST_7_DAYS`.

**Pipedrive (cruzar leads reais):** token em `.env` raiz / CLAUDE.md. Filtrar label `68477770-00da-11f0-aacd-39462ebe07ed`.

---

## 8. Formato de entrega (regra William)

- **Dashboard HTML standalone** em `clientes/silva-pimenta/marketing/trafego-pago/otimizacoes/auxilio-moradia/YYYY-MM-DD/` com `INDEX.html` + `analises/01-google-ads.html` (+ `02-meta-ads.html` quando rodar Meta).
- Paleta da marca: teal `#1A4758` + champagne `#C5A57A` + bege `#f7f5f0`, fonte Jost.
- Estrutura: KPIs no topo (cards) → comparativo 30/14/7 → achados (bom/ruim com cor) → 7 passos → **plano em 3 camadas (hoje / esta semana / próximas 2 semanas)** → regras respeitadas.
- **Sempre 14d vs 7d** + botão copiar nas negativas.
- Entrega antiga = histórico, não regerar (memory `feedback_propostas_relatorios_historico`). Pasta nova por data.

---

## 9. Critério de sucesso (confere ANTES de entregar)

- [ ] Passo 0 (anúncio APPROVED?) e Passo 1 (goals biddable certos?) checados ANTES de analisar métrica.
- [ ] Leads reais cruzados com Pipedrive (não só "conversions" do Google).
- [ ] 30/14/7 puxados da API, não estimados.
- [ ] CPL comparado à régua REAL R$ 76 (não a aspiracional).
- [ ] Nenhuma recomendação de pausar/matar a campanha Google (§2).
- [ ] Nenhuma negativa de cidade nem de termo direto do produto.
- [ ] Plano em 3 camadas + flag OAB. Zero travessão.
- [ ] Dashboard HTML datado salvo na pasta certa.
