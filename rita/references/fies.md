# Playbook Rita · FIES (Silva Pimenta)

> **LER ANTES de qualquer relatório/otimização do FIES.** Este arquivo é a inteligência específica do produto: contas, sub-produtos, régua real, armadilhas vividas e regras invioláveis. O Gabarito ADAPTA e as skills de análise continuam valendo por cima disto. Última calibragem: 09/06/2026.
>
> **Verificação em cadeia:** os IDs abaixo foram lidos da API em 26/05/2026 e revalidados em 09/06/2026. Campanha pode ser excluída/recriada; sempre **resolver por NOME** e confirmar o ID na hora. Tratar os IDs daqui como atalho, não como verdade eterna.

---

## 1 · O produto em 30 segundos

O FIES do Silva Pimenta é **4 sub-produtos enrolados num único site** — é a primeira coisa que precisa entrar na cabeça antes de olhar qualquer métrica:

| Sub-produto | Avatar | Dor | Volume real (Google 14d) |
|---|---|---|---|
| **Abatimento FIES Médico** | médico formado 26-40 com FIES ativo | "minha dívida não diminui mesmo pagando" | baixo · termo direto do produto |
| **Reduzir Dívida FIES** | médico em atraso ou com bola de neve | "preciso negociar pra sair do vermelho" | **DOMINA** · 78% das conversões |
| **FIES COVID/Pandemia** | médico que atuou no SUS 2020-2022 | "ouvi falar que tenho direito a abatimento" | médio · melhor CPA da conta |
| **Suspensão FIES** | residente com bolsa baixa que precisa pausar | "não consigo pagar enquanto residente" | **FORA DO AR** · sub-produto descoberto |

- **Regra fundamental:** os 4 sub-produtos têm **públicos, dores e LPs distintos**. Tratar tudo como "FIES" no relatório é o caminho mais curto pra concluir errado. Sempre separar performance por AD GROUP (que corresponde a sub-produto), não só por campanha.
- **Atuação NACIONAL.** Cidade no termo nunca é desqualificação.
- **Adimplência é REQUISITO LEGAL** pra requerer abatimento (lei exige). Termo "adimplente", "em dia", "paga em dia" é o avatar QUALIFICADO, não lixo a negativar.
- **Canais ativos hoje:** apenas Google Search. Meta foi falado mas não está implantado pra FIES (15/06).
- **Meta de operação:** ainda não tem número fechado; calibrar quando William definir.

---

## 2 · A TESE ESTRATÉGICA (o aprendizado central)

**FIES é produto de BUSCA com 1 sub-produto dominante e 1 sub-produto morto.**

- **Reduzir Dívida** é o motor: a keyword `"reduzir dívida fies"` (frase) sozinha trouxe 13 conversões em 14d com CPA R$ 60. É o termo de maior intent + maior volume da conta. **Esse é o produto principal hoje, não o "Abatimento Médico".**
- **Abatimento FIES Médico** é termo do produto mas **0 conv há semanas** (15 cliques · R$ 115/14d, depois 44 cliques · R$ 371 no ciclo anterior). Diagnóstico fechado: **a LP genérica `/fies/` não confirma o ângulo** que o termo promete. Solução é LP específica, não pausa (regra §6).
- **COVID/Pandemia** é o tesouro escondido: AD GROUP 2 Brasil tem o **menor CPA da conta (R$ 40)**. Volume pequeno mas alta intent. Quando subir a LP `/fies/covid/`, esse grupo deve escalar.
- **Suspensão FIES** está **fora do ar** — sub-produto sem cobertura. Não tem campanha rodando. Decisão pendente: ativar campanha dedicada ou confirmar exclusão estratégica.

**Implicação pro relatório:**
- Conversões altas + CPA baixo do AD GROUP 3 (Reduzir Dívida) **escondem** o problema do AD GROUP 1. Sempre desagregar.
- "Mais budget" não resolve nada antes da LP nova subir — Lost IS por classificação é 49%, Lost IS por orçamento é 21%. **Gargalo é QS, não dinheiro.**

---

## 3 · Mapa de contas e IDs (puxar sem perguntar)

### Google Ads — customer `5313139497` ("Silva Pimenta - [FIES]")

| Campanha | ID | Status | Orçamento/dia | Papel |
|---|---|---|---|---|
| `Pesquisa - [FIES] - Brasil` | `20766284775` | ENABLED | R$ 112 | Principal (78% do gasto) |
| `Pesquisa - [FIES] - SP` | `20772411575` | ENABLED | R$ 15 | Recorte SP (CPC mais caro) |
| `P MAX - FIES` | `22106329114` | PAUSED | R$ 75,68 | "Limitada pela política" — investigar |
| `YT | LEADS | FIES #2` | `23318334882` | PAUSED | Demand Gen fora do ar |

**MCC pai:** `9025188297` (todas as contas do Silva Pimenta + Magalhães Gomes).

### Ad Groups ativos (resolver por NOME, ID é atalho)

| Campanha | Ad Group | ID | Sub-produto | Status real |
|---|---|---|---|---|
| Brasil | **AD GROUP 3: Reduzir Dívida FIES** | `197925887480` | Reduzir Dívida | EXCELENTE (CPA R$ 77) |
| Brasil | **AD GROUP 2 — FIES COVID / Pandemia** | `194756819225` | COVID | MELHOR CPA da conta (R$ 40) |
| Brasil | **AD GROUP 1: Abatimento FIES Médico** | `193185999497` | Abatimento Médico | ZERO conv crônico |
| SP | AD GROUP 2 — FIES COVID / Pandemia | `195090164869` | COVID | OK (R$ 88) |
| SP | AD GROUP 1: Abatimento FIES Médico | `195090164789` | Abatimento Médico | ZERO conv |

### Conversion goals — **VALIDAR EM TODA RODADA**

Conta usava "Botão WhatsApp" como sinal. Em 26/05 ficou aberto:
- Confirmar via API qual é a conversão `biddable` em `campaign_conversion_goal` (ver Passo 1 da §5).
- LP atual `silvapimenta.com.br/fies/` dispara só o WhatsApp (NÃO tem formulário ainda — gargalo conhecido).
- Quando as LPs novas subirem (covid/abatimento-medico/reduzir-divida), a conversão "FIES — Form Lead" precisa ser criada como primária + biddable, com Enhanced Conversions ON.

### Landing pages

**LP atual (ainda no ar):** `https://silvapimenta.com.br/fies/`
- WordPress + Elementor. Lenta (Core Web Vitals reprovados).
- Genérica pra 3 ângulos. Hero não converte por ângulo.
- Sem formulário inline (só botão WhatsApp).
- **É a raiz do gargalo de QS** (ver §4).

**LPs novas (criadas em 05/05, NÃO subidas no WordPress até 09/06):**
- `/fies/covid/` (ângulo Lei 14.375/22, destino AD GROUP 2)
- `/fies/abatimento-medico/` (4 modalidades, destino AD GROUP 1)
- `/fies/reduzir-divida/` (dor financeira + tabela comparativa, destino AD GROUP 3)
- Master + guia WordPress completo em `clientes/silva-pimenta/marketing/trafego-pago/otimizacoes/fies/2026-05-05/`

**Pendência crítica:** subir as 3 no WordPress. Enquanto não subirem, QS continua travado em 2-3 e CPA não cai abaixo de R$ 50.

### Lista de negativas

**Aplicação:** negativas estão **por campanha** (não em lista compartilhada). Total ~58 termos após ciclo 26/05.
- 52 negativas aplicadas em 05/05 (Desenrola Brasil, anistia, perdão, 99%, não-médico, informacionais, mídia).
- 6 criterios adicionados em 26/05: `"g1"`, `"g1 desconto fies"`, `"g1 fies desconto"` em ambas campanhas.
- **NÃO negativar:** adimplentes (requisito legal), "desconto fies" (typo de abatimento), cidades, termos do produto, "negociar fies" (descoberto como convertedor).

---

## 4 · Benchmarks REAIS do produto (a régua de verdade)

O `benchmarks-br.md` genérico de Google Search dá CPL R$ 50-90, mas o FIES tem régua observada própria. Usar ESTES números:

| Métrica | Régua real do FIES | Leitura |
|---|---|---|
| **CPA 14d (saudável)** | R$ 50 a 90 | dentro do esperado pra busca de alta intent |
| **CPA 14d (atenção)** | R$ 90 a 130 | subiu — investigar tracking ou LP |
| **CPA 14d (crítico)** | > R$ 130 | zona vermelha — diagnóstico imediato |
| **CPA atual** | R$ 80 (14d) / R$ 57 (7d) — após 52 negativas | saudável, tendência boa |
| **CPC médio** | R$ 5,50 a 7,50 | normal pro nicho; SP fica em R$ 12-17 (leilão SP mais caro) |
| **CTR de busca** | 6,5% a 7,5% | acima do range 3-6% do genérico, sinal de copy/intent boa |
| **Taxa de conversão** | 7% a 10% (após melhorias) · 4-5% (antes) | boa quando LP nova subir |
| **QS médio (baseline 14d)** | 2-3 — 100% das keywords com LP "abaixo da média" | meta: chegar a 5-6 após LP nova |
| **Lost IS por classificação** | 49% (Brasil) · 20% (SP) | gargalo dominante no Brasil |
| **Lost IS por orçamento** | 21% (Brasil) · 53% (SP) | só SP precisa de mais budget |
| **Search IS** | 40% | razoável; vai subir com QS melhor |
| **Volume de buscas (nicho)** | ~4.800 impressões/14d | termos de cabeça: "reduzir dívida fies" 154 cliques, "abater dívida fies" 73 cliques |

**Não confundir:**
- Lost IS por classificação alta = QS/AdRank ruim. **NÃO mexer orçamento** — paga mais caro pra seguir mal posicionado.
- Lost IS por orçamento alta = subir budget pode fazer sentido. Só SP cai nesse caso.

### Distribuição que sempre vale a pena ler

- **Device:** 80% mobile · 20% desktop. CPA mobile R$ 77, desktop R$ 90. **LP precisa ser mobile-first absoluta.**
- **Hora do dia (pico):** 11h-16h concentra 70% das conversões.
- **Hora do dia (CPA campeão):** 6h da manhã tem CPA R$ 40. 8h tem CPA R$ 109 (transição/trânsito).

---

## 5 · As 7 armadilhas históricas (diagnóstico diferencial)

Quando o relatório mostrar comportamento estranho, rodar esta lista ANTES de propor mudança. Todas já aconteceram:

1. **Anúncio reprovado por política do FIES:** P MAX já caiu por isso ("Limitada pela política"). Sempre rodar o Passo 0 (`policy_summary.approval_status`) antes de qualquer análise. Quando reprovado, métrica vira ruído.

2. **Conversion goal apontando pra lugar errado:** a LP atual `/fies/` dispara só o evento WhatsApp. Quando subir as LPs novas com formulário, o `campaign_conversion_goal.biddable` precisa apontar pra "FIES — Form Lead" também. Se ficar só no clique do WhatsApp, leads de formulário não otimizam o bidding.

3. **"Conversions" do Google ≠ leads reais:** sempre cruzar com Pipedrive (label FIES — confirmar ID no `.env`). Já teve volume de "conversões" no Google sem deal correspondente no Pipedrive nos mesmos dias (23-26/05 teve 4 dias com 0 conv reportada mas R$ 432 gastos — preciso conferir Pipedrive nesse período).

4. **AD GROUP 1 (Abatimento Médico) zero conv crônico** sem ser bug: o termo é direto do produto mas a LP genérica não confirma o ângulo. **Não pausar** (regra §6) — corrige via LP nova `/fies/abatimento-medico/`.

5. **`ONE_WEBSITE_PER_AD_GROUP`:** mesma armadilha do Auxílio Moradia e Direito Médico. Todos os RSAs (ENABLED **e** PAUSED) do Ad Group têm que apontar pro MESMO domínio raiz. Quando trocar URL pra LP nova, conferir TODOS os RSAs. Se subir LPs como `silvapimenta.com.br/fies/covid/` (subdomínio do site), zero risco. Se subir como `fies-covid.silvapimenta.com.br` (subdomínio próprio), conferir.

6. **"Desconto fies" e "adimplentes" NÃO são lixo:** já tive a tentação de negativar. Adimplência é REQUISITO LEGAL do produto (memória `project_silva_pimenta_fies_adimplencia`). "Desconto fies" é typo natural de "abatimento fies" (memória do William, 05/05). Termo "desconto do fies" CONVERTEU com CPA R$ 9 no ciclo 26/05.

7. **Volatilidade de fim de semana:** dias 23-26/05 teve 4 dias com 0 conv mas R$ 432 gastos. Sábado/domingo + segunda. Pode ser delay de tracking ou variação natural. Sempre conferir Pipedrive nos dias zerados antes de alarmar.

---

## 6 · Regras invioláveis (o que a Rita NUNCA recomenda)

- **NUNCA negativar "adimplentes / em dia / paga em dia / desconto fies / fies adimplentes / para adimplentes"** — adimplência é requisito legal, qualifica o avatar (memória `project_silva_pimenta_fies_adimplencia`).
- **NUNCA pausar AD GROUP 1 (Abatimento FIES Médico)** mesmo com zero conv crônico. Termo é direto do produto e captura o avatar mais qualificado. Solução é LP nova + RSA reescrito + QS subindo (memória `project_silva_pimenta_fies_ad_group_relevancia`).
- **NUNCA pausar campanha cara que traz lead qualificado.** Otimização por QUALIDADE, não por CPL isolado. Decidir por vendas + tags Pipedrive (memória `feedback_otimizacao_por_qualidade_nao_cpl`).
- **NUNCA negativar cidade** — atuação nacional (memória `feedback_nao_negativar_cidades_atuacao_nacional`).
- **NUNCA negativar termo direto do produto** ("abatimento fies", "reduzir divida fies", "negociar fies"). Termo que não converte se corrige por LP/RSA/QS.
- **OAB: flag SEMPRE, NÃO impõe pausa** — William assume risco regulatório conscientemente. Headlines "100%", "30 dias", "Zere sua dívida" continuam ativas (memória `feedback_oab_silva_pimenta_risco_assumido`). Concorrentes (Marcel Zeferino, AM Advocacia Médica, Luan Mazza) usam linguagem similar.
- **NUNCA propor cartoon** em copy/criativo (memória `feedback_estilo_cartoon_evitar`).
- **NUNCA usar travessão** em qualquer texto (memória `feedback_sem_travessoes`).
- **NUNCA inflar números reais.** Os auditáveis do escritório: +500 médicos defendidos, 98% aprovação, 256 reviews Google 5★, +20 anos (memória `project_silva_pimenta_numeros_aux_moradia` — valem pro FIES também).
- **Ritmo híbrido obrigatório:** check semanal **observa**, mudança estrutural só a cada 14 dias (memória `project_direito_medico_ritmo_hibrido` — vale também pro FIES). Não empilhar mudança sobre mudança recente.
- **Sempre desativar Parceiros de Pesquisa e Display** em campanha Search (memória `feedback_google_ads_redes_desativar`). Script `create.py` vem com Parceiros ON por default, corrigir após criar.

---

## 7 · Passada da apostila adaptada ao FIES (ordem)

Pré-checagem do SKILL roda antes de qualquer um destes:

1. **Search terms** (`read.py search-terms`, janela do relatório) cruzado com negativas existentes:
   - Termo novo que CONVERTE não keyword → propor adicionar como keyword no AD GROUP correto.
   - Termo lixo → negativar a frase específica (não o token solto que pode ser do produto).
   - Cuidar regras §6: nunca "adimplentes", "desconto fies", cidades, termos do produto.
   - **Caso especial FIES:** termo com "negociar" descoberto em 26/05 como convertedor — keywords já adicionadas. Validar performance.

2. **Quality Score decomposto** (`read.py quality-scores`): separar `creative_quality_score` / `post_click_quality_score` / `search_predicted_ctr`.
   - **Hoje (09/06):** 100% das keywords ativas com `post_click = BELOW_AVERAGE`. Creative quality boa (Acima em 8 de 14). CTR esperado abaixo em todas — consequência da LP.
   - Reportar distribuição (quantas QS 1/2/3/4/5+).
   - Meta após LP nova: chegar a QS médio 5.

3. **Parcela de impressão:** ler as duas perdidas. Brasil 49% classificação + 21% orçamento → mexer LP, não verba. SP 53% orçamento + 20% classificação → aqui faz sentido subir verba.

4. **Performance por AD GROUP** (CRÍTICO no FIES — não agregar por campanha):
   - AD GROUP 3 (Reduzir Dívida): a galinha dos ovos de ouro. Manter rodando, observar saturação.
   - AD GROUP 2 (COVID): segundo melhor. Quando LP `/fies/covid/` subir, vai escalar.
   - AD GROUP 1 (Abatimento Médico): zero conv crônico. NÃO pausa. Esperar LP nova.

5. **Correspondências:** frase/exata. Hoje a frase "reduzir divida fies" performa muito; a exata `[reduzir divida fies]` tem QS 2. Quando LP nova subir, vale subir lance da frase e reativar a exata.

6. **Lance:** Estratégia atual a confirmar via API (`campaign.bidding_strategy_type`). Provavelmente Maximize Conversions. Com volume de 23 conv/14d, ela funciona. Se mudar pra tCPA, validar histórico.

7. **Anúncios/extensões:**
   - RSAs ativos têm OAB-borderline mantidas (decisão consciente).
   - Sitelinks/callouts ativos? Conferir.
   - **Ad Strength:** todos em "Na média" no ciclo 05/05. Headlines repetidas. Quando reescrever, atualizar pelo menos 4 headlines novas com palavras-chave variadas.

8. **Higiene:** Parceiros de Pesquisa OFF, Display Network OFF. **Sempre conferir** — `create.py` vem com Parceiros ON.

9. **Device + hora + dia** (se volume permitir): mobile dominante, pico 11h-16h, 6h da manhã com CPA campeão. Vale aplicar bid schedule +20% em 5h-7h e -15% em 8h-9h via Programação.

---

## 8 · Checklist cirúrgico — o que olhar em TODO relatório de FIES

- [ ] **Pré-checagem do SKILL** (anúncio APPROVED? conversão biddable certa? lead real no Pipedrive?) ANTES de qualquer métrica.
- [ ] **Lead REAL contado no Pipedrive** (label FIES — confirmar `.env`), não só "conversions" do Google.
- [ ] **Performance por AD GROUP separada** (não agregar por campanha — FIES é 4 sub-produtos).
- [ ] **QS decomposto:** quantas com LP BELOW_AVERAGE? Tendência vs baseline 100%.
- [ ] **Lost IS:** classificação vs orçamento por campanha. Brasil é QS; SP é budget.
- [ ] **Search terms novos:** convertedores não-keyword (adicionar) e lixos óbvios (negativar dentro das regras §6).
- [ ] **Status das 3 LPs novas:** subiram no WordPress? Mudaram URL final dos RSAs por AD GROUP correspondente? Conversion goal nova criada?
- [ ] **Decisão Suspensão FIES:** ativar campanha dedicada ou confirmar exclusão? Sub-produto sem cobertura há semanas.
- [ ] **P MAX:** investigar bloqueio por política — vale tentar reativar?
- [ ] **Tendência 30 → 14 → 7** pra separar causa de efeito.
- [ ] **Flag OAB** nas peças/extensões.

---

## 9 · Estrutura do relatório de FIES (HTML cirúrgico)

Seguir o modelo da Rita, com estas seções específicas:

1. **KPIs topo:** CPA · conversões · CTR · gasto total · Search IS · QS médio. **Sempre 14d × 7d.**
2. **Comparativo cíclico:** 14d atual vs 14d anterior (mudanças). Esperar ler efeito de ciclos passados (05/05 e 26/05).
3. **Performance por AD GROUP** (não por campanha): tabela com CPA, conversões, status (excelente/saudável/crítico) por sub-produto. **Esta é a seção central do FIES** — onde a complexidade real aparece.
4. **Search terms:**
   - Termos novos que converteram (candidatos a keyword).
   - Termos com gasto sem conv (candidatos a negativa — passar pelo filtro §6 antes de propor).
   - Box com botão copiar nas negativas a aplicar.
5. **Quality Score decomposto:** tabela das top keywords com QS, creative, LP, CTR esperado. Mostra o gargalo da LP claramente.
6. **Lost IS por campanha:** classificação vs orçamento. Decisão de mexer budget só onde orçamento for o gargalo.
7. **Insights profundos (quando volume permitir):** device, hourly heatmap, daily trend (sparkline da curva).
8. **Status das LPs novas:** pendentes? subidas? URLs apontadas? Conversion goal ativa?
9. **Bom / Ruim / Recomendações pra aprovar** em 3 camadas:
   - **HOJE:** ações via API que a Rita pode aplicar direto (negativas óbvias dentro das regras, keywords novas de termos descobertos, bid schedule).
   - **ESTA SEMANA:** decisões que dependem do William ou de implementação WordPress (subir LPs, criar conversion goal nova, mudar URL final dos RSAs).
   - **PRÓXIMAS 2 SEMANAS:** estratégico (Suspensão FIES sim/não, investigar P MAX, A/B test de copy OAB-safe).
10. **Pendências e decisões em aberto.**

**Onde salvar (padrão da casa):** pasta datada `clientes/silva-pimenta/marketing/trafego-pago/otimizacoes/fies/YYYY-MM-DD/` com `INDEX.html` navegável + `analises/01-google-ads.html` (+ `02-meta-ads.html` quando Meta entrar) + `dados/` (todos os JSONs da API + audit log) + `assets/` (logo + hero).

Paleta da marca: teal `#1A4758` + champagne `#C5A57A` + bege `#f7f5f0`. Fontes Playfair Display + Montserrat (ou Jost se for padrão Rita).

**Sempre 14d × 7d** + botão copiar nas negativas. Entrega antiga é histórico, **não regerar** — pasta nova por data.

---

## 10 · Comandos de API prontos (copy-paste, rodar da raiz do workspace)

```bash
CID=5313139497   # Google Ads FIES

# Métricas por campanha (rodar LAST_30_DAYS / 14 / 7)
python .claude/skills/google-ads-ratos/scripts/read.py campaigns --customer-id $CID --date-range LAST_14_DAYS
python .claude/skills/google-ads-ratos/scripts/read.py campaigns --customer-id $CID --date-range LAST_7_DAYS
python .claude/skills/google-ads-ratos/scripts/read.py campaigns --customer-id $CID --date-range LAST_30_DAYS

# Ad Groups (separar AD GROUP 1/2/3 — não agregar por campanha)
python .claude/skills/google-ads-ratos/scripts/insights.py ad-group --customer-id $CID --date-range LAST_14_DAYS

# Keywords + Quality Score
python .claude/skills/google-ads-ratos/scripts/insights.py keyword --customer-id $CID --date-range LAST_14_DAYS
python .claude/skills/google-ads-ratos/scripts/read.py quality-scores --customer-id $CID

# Search terms (desperdício)
python .claude/skills/google-ads-ratos/scripts/read.py search-terms --customer-id $CID --date-range LAST_14_DAYS

# Anúncios (RSAs)
python .claude/skills/google-ads-ratos/scripts/read.py ads --customer-id $CID --date-range LAST_14_DAYS

# Negativas atuais (confirmar aplicação)
python .claude/skills/google-ads-ratos/scripts/read.py negative-keywords --customer-id $CID

# Insights profundos
python .claude/skills/google-ads-ratos/scripts/insights.py device --customer-id $CID --date-range LAST_14_DAYS
python .claude/skills/google-ads-ratos/scripts/insights.py hourly --customer-id $CID --date-range LAST_30_DAYS
python .claude/skills/google-ads-ratos/scripts/insights.py daily --customer-id $CID --date-range LAST_30_DAYS
```

**Encoding Windows:** sempre prefixar `PYTHONIOENCODING=utf-8` ou ler arquivo com `errors='replace'` no parse — saídas têm caracteres especiais (acentos das keywords) que quebram cp1252.

**Aplicar mudanças (via API, com aprovação do William):**
```bash
# Adicionar negativa em campanha
python .claude/skills/google-ads-ratos/scripts/create.py negative \
  --customer-id $CID --campaign-id 20766284775 \
  --text "termo lixo" --match-type PHRASE

# Adicionar keyword nova em ad group
python .claude/skills/google-ads-ratos/scripts/create.py keyword \
  --customer-id $CID --ad-group-id 197925887480 \
  --text "negociar fies" --match-type PHRASE

# Mudar URL final do RSA (quando LPs novas subirem)
# update.py ad --customer-id ... --ad-id ... --final-urls https://silvapimenta.com.br/fies/covid/
```

**GAQL custom** (via `lib.run_query`) pra o que `read.py` não cobre:
- Status de aprovação do anúncio (Passo 0): `SELECT ad_group_ad.policy_summary.approval_status FROM ad_group_ad`
- `campaign_conversion_goal.biddable` por campanha (Passo 1)
- `conversion_action` + tag_snippets pra achar label
- Histórico diário (`segments.date`)
- Device (`segments.device`)
- Schedule de horários atual

**Atenção:**
- Orçamento Google em **MICROS** (R$ 50 = 50.000.000 micros). Diferente do Meta (centavos).
- `LAST_2_DAYS` não existe no GAQL — usar datas absolutas (`segments.date BETWEEN '2026-06-07' AND '2026-06-09'`) ou `LAST_7_DAYS`.

**Pipedrive (lead real):** token `PIPEDRIVE_TOKEN` no `.env` central. **Confirmar label FIES** no Pipedrive (não estava documentado em 09/06). Filtro de data em Brasília (UTC-3, memória `feedback_pipedrive_timezone_brasilia`).

---

## 11 · Decisões já tomadas (não relitigar)

- **52 negativas aplicadas em 05/05** (Desenrola/Anistia/99%/não-médico/informacionais/mídia). NÃO incluir adimplentes nem "desconto fies" — decisão consciente.
- **AD GROUP 1 Abatimento Médico NÃO pausa** apesar de zero conv crônico. Termo é direto do avatar.
- **Headlines OAB-borderline mantidas** ("100%", "30 dias", "Zere sua dívida") — risco assumido conscientemente.
- **3 LPs criadas em 05/05** (covid, abatimento-medico, reduzir-divida) — pendentes de upload no WordPress. Guia completo em `2026-05-05/guias/01-guia-wordpress.html`.
- **6 negativas G1 + 5 keywords "negociar"** aplicadas em 26/05 via API. Audit em `2026-05-26/dados/audit-log.txt`.
- **WhatsApp atual:** (11) 97716-7482 (memória `project_silva_pimenta_whatsapp_numero` — voltou do ban em 12/06).
- **Próximas LPs no WordPress:** Elementor Canvas (não Tema), WPForms enviando pra 3 e-mails (contato@ + william@ + maria.eduarda@silvapimenta.com.br), `/obrigado-fies/` noindex com tag de conversão.
- **Suspensão FIES pendente:** sub-produto sem campanha. Decidir ativar ou confirmar exclusão.
- **PMax bloqueada por política** — investigar quando tiver tempo.

---

## 12 · Cadência e datas-âncora

- **Terça = dia de FIES** (cadência semanal da Rita).
- **Ciclos estruturais a cada 14 dias** (regra híbrida). Checks semanais entre estruturais SÓ observam, não intervêm (exceto emergência: CPA > R$ 130 ou conv 7d < 7).
- **Baselines pra comparar:**
  - **05/05 (estrutural):** CPA R$ 161 (14d) — antes das 52 negativas.
  - **26/05 (estrutural):** CPA R$ 80 (14d) / R$ 57 (7d) — após negativas, antes das LPs.
  - **09/06 (estrutural):** marco da próxima leitura — esperar efeito das 12 ações do 26/05 (negativas G1 + keywords negociar + [exact] diminuir).
  - **Próximo (23/06):** esperar LPs novas terem subido e QS começado a reagir.
- **Mudanças estruturais grandes:** 05/05 (52 negativas + 3 LPs criadas), 26/05 (3 negativas G1 + 5 keywords negociar + 1 exata + bid schedule discutido). Ler efeito 7-14 dias depois de cada.

---

## 13 · Critério de sucesso (confere ANTES de entregar)

- [ ] **Pré-checagem do SKILL rodada** (anúncio APPROVED? conversão biddable correta? lead real no Pipedrive?) ANTES de qualquer métrica.
- [ ] **Performance por AD GROUP separada** — FIES é 4 sub-produtos, agregação por campanha esconde a verdade.
- [ ] **Lead REAL contado no Pipedrive** (label FIES — confirmar ID), não só "conversions" do Google.
- [ ] **30/14/7 puxados da API**, não estimados.
- [ ] **CPA comparado à régua REAL** (R$ 50-90 saudável), não ao genérico do `benchmarks-br`.
- [ ] **QS decomposto** mostrando que LP é gargalo (espera-se 100% BELOW_AVERAGE até as LPs novas subirem).
- [ ] **Lost IS por classificação vs orçamento** — Brasil não precisa de mais budget, SP precisa.
- [ ] **Status das 3 LPs novas registrado** no relatório (subiram? URL final dos RSAs apontada?).
- [ ] **Nenhuma negativa de cidade nem de termo de produto nem de adimplência** — ler regras §6.
- [ ] **Nenhuma recomendação de pausar AD GROUP 1** mesmo com zero conv.
- [ ] **Plano em 3 camadas + flag OAB** (sem impor pausa). Zero travessão.
- [ ] **Dashboard HTML datado** salvo na pasta certa com `INDEX.html` + `analises/` + `dados/` + `assets/`.
- [ ] **Audit log salvo** se houve aplicação via API.
- [ ] **Entrada no `atividades-recentes.md`** com `/fechar-sessao` no fim.
