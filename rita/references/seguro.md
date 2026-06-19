# Playbook Rita · SEGURO (Magalhães Gomes)

> **LER ANTES de qualquer relatório/otimização de Seguro.** Este arquivo é a inteligência específica do produto: as 2 contas, sub-produtos, régua real, armadilhas já vividas e regras invioláveis. O Gabarito ADAPTA e as skills de análise continuam valendo por cima disto. Primeira calibragem completa: 12/06/2026 (primeira leitura limpa pós-correção de tracking de 27/05).
>
> **Atenção ao cliente:** Seguro é **Magalhães Gomes**, não Silva Pimenta. Cliente civil (leigo), não médico. Tom, contas, Pipedrive e pastas são do Magalhães. Confundir com a inteligência do médico é o erro mais fácil de cometer aqui.
>
> **Verificação em cadeia:** os IDs abaixo foram lidos da API em 12/06/2026. Campanha pode ser excluída/recriada — sempre **resolver por NOME** e confirmar o ID na hora. Tratar os IDs daqui como atalho, não como verdade eterna.

---

## 1 · O produto em 30 segundos

O Seguro do Magalhães Gomes é **defesa do segurado**: quando a seguradora nega, atrasa ou paga menos, o escritório reverte. São **2 sub-produtos** rodando nas campanhas de Google (LIVRE-IR é conta à parte e foi descontinuado em 26/05, não entra aqui):

| Sub-produto | Avatar | Dor | Volume real (Google 16d) |
|---|---|---|---|
| **SEGURO (guarda-chuva)** | civil com carro/casa/rural/máquina e sinistro negado | "a seguradora não me pagou a indenização" | **DOMINA** · veicular é o motor |
| **SEG VIDA** | beneficiário (família) com seguro de vida negado | "negaram por doença preexistente / carência / atraso" | médio · CPA mais caro, ticket maior |

- **REGRA DE OURO do produto:** o escritório defende o **SEGURADO contra a seguradora**. Quem busca "fazer seguro", "cotação", "2ª via", "telefone da seguradora", "cancelar seguro" é **cliente da seguradora, não da gente** — é lixo, não lead.
- **Atuação NACIONAL.** Cidade no termo nunca é desqualificação (mesmo em campanha "SP" ou "MG").
- **Canais ativos hoje:** apenas **Google Search** nas 2 contas. Meta roda Livre-IR (produto à parte) e tem campanhas de Seguro/Seg Vida a confirmar BM (pendência do CLAUDE.md). Este playbook é **Google-first**; quando Meta de Seguro for mapeado, anexar aqui.
- **Público civil leigo:** tom didático e empático (diferente do "par-a-par com médico" do Silva Pimenta). Vale pra qualquer copy/LP proposta no relatório.

---

## 2 · A TESE ESTRATÉGICA (o aprendizado central)

**Seguro roda em 2 contas Google DUPLICADAS DE PROPÓSITO, e a conta Contingência está estruturalmente mais cara que a Institucional pelas MESMAS keywords.**

1. **As 2 contas são intencionais, NUNCA consolidar.** Institucional (`1301598996`) e Seguro Contingência (`2903149800`) rodam estrutura quase idêntica de propósito: **cobertura de leilão**. Quando uma perde o leilão, a outra tenta ganhar. Decisão reforçada pelo William em 27/05 (memória `project_magalhaes_gomes_duas_contas_proposital`). Propor fundir as duas é recomendação inválida.

2. **VEICULAR é a galinha dos ovos de ouro, e está estrangulada.** Nas 2 contas, as campanhas VEICULAR têm o melhor CPA (R$ 19 a 31) e **perdem 21% a 41% das impressões por ORÇAMENTO**. É onde mais budget rende lead barato.

3. **A Contingência paga CPC de 2× a 4× a Institucional nas mesmas keywords.** Causa raiz: a Inst tem teto de CPA (tCPA R$ 50-60) nas campanhas SEGURO e VIDA; a Cont roda **Maximizar Conversões SEM teto** em 5 de 7 campanhas. Sem teto, o Smart Bidding compra topo absoluto a qualquer preço (Cont VIDA 05: IS 89%, topo absoluto 79%, CPC R$ 41 vs R$ 9 da Inst). **Definir tCPA na Cont é a maior alavanca de eficiência da operação.**

4. **A LP é o gargalo de Quality Score.** As keywords mais caras (advogado especialista em seguros, advogado securitário, ações contra seguradoras, e o grupo SEGURO DE VIDA NEGADO inteiro) têm QS 1 a 3 com **"experiência na página" abaixo da média**. As LPs atuais são genéricas, rasas (110-180 palavras), pesadas (1+ MB) e algumas com bug grave (ver §5). 3 LPs novas foram criadas em 12/06 (ver §3) pra atacar isso.

**Implicação pro relatório:**
- **Sempre desagregar por conta E por campanha.** O CPA médio combinado esconde que a Cont é quase 2× a Inst. Reportar as duas lado a lado.
- "Mais budget" só resolve onde a perda é por ORÇAMENTO (as VEICULAR). Onde a perda é por CLASSIFICAÇÃO (SEGURO/VIDA da Cont, SEGURO MG/SP), o remédio é tCPA + QS, **nunca verba**.
- **A conversão do Google é clique de WhatsApp/chamada, NÃO lead qualificado** (ver §3). CPA de R$ 19 não quer dizer lead de R$ 19.

### Protocolo de teste vigente (decisão do William, 12/06/2026) — RESPEITAR

> William definiu: **testar TUDO primeiro na conta Contingência** (a pior), começando pelas LPs novas, depois as ações (tCPA, negativas, realocação). Só se a Cont melhorar é que replica na Institucional.

- Não aplicar mudança na Inst antes da Cont validar. Relatório de Seguro nesse período mede **Cont isolada** como termômetro do teste, com a Inst de grupo de controle.
- Ordem do teste: **(1) LPs novas no ar → (2) trocar URL final dos ad groups da Cont → (3) validar GTM dispara → (4) tCPA + negativas + realocação na Cont → (5) ler 7-14d → (6) replicar na Inst se melhorou.**

---

## 3 · Mapa de contas e IDs (puxar sem perguntar)

**MCC pai:** `9025188297` (Think Lab — todas as contas do escritório). Auto-tagging (gclid) **ATIVO nas 2 contas** (confirmado API 12/06) — habilita o tracking de fechamento da §11.

### Conta A — INSTITUCIONAL · customer `1301598996` ("Magalhães Gomes Advogados")

| Campanha | ID | Budget/dia | Lance | CPA 16d | Papel |
|---|---|---|---|---|---|
| `NEGATIVA VEICULAR \| BRASIL - SP \| 00` | `20884487883` | R$ 220 | Maximizar cliques | **R$ 19,10** | CAMPEÃ (178 conv) |
| `NEGATIVA VEICULAR \| SP \| 01` | `21124850528` | R$ 160 | Maximizar cliques | R$ 25,84 | forte (91 conv) |
| `NEGATIVA SEGURO \| BRASIL - SP & MG \| 02` | `21519123483` | R$ 240 | Max conv · tCPA R$ 50 | R$ 49,41 | cara (71 conv) |
| `NEGATIVA SEGURO \| SP \| 03` | `21519123486` | R$ 80 | Max conv · tCPA R$ 50 | R$ 42,99 | recorte SP |
| `NEGATIVA SEGURO \| MG \| 04` | `21562555811` | R$ 120 | Max conv · tCPA R$ 60 | R$ 37,58 | budget ocioso (gasta R$ 31/d) |
| `NEGATIVA VIDA \| BRASIL - SP & MG \| 05` | `22644361834` | R$ 86 | Max conv · tCPA R$ 50 | R$ 37,47 | vida |
| `NEGATIVA VIDA \| SP & MG \| 08` | `22919090286` | R$ 117 | Max conv · tCPA R$ 60 | R$ 25,46 | vida (budget ocioso) |

PAUSADAS: `NEGATIVA MÁQUINA \| BRASIL` (23036115584, pausada por baixo volume 27/05), 2 testes veicular (06/07), 1 Demand Gen vídeo. **NEG MÁQUINA não reativar sem decisão** (memória `project_magalhaes_gomes_*`: pausada por falta de volume).

- **Conversões ENABLED (confirmado API 12/06):** `CONTATO WHATSAPP` (CONTACT, primary) + `Envio Formulario` (SUBMIT_LEAD_FORM, primary). As 2 contam intenção, não conversa efetiva.
- **Total 16d (28/05-12/06):** R$ 722/dia · 401 conv · CPA médio R$ 28,83.

### Conta B — SEGURO CONTINGÊNCIA · customer `2903149800` ("MAGALHAES GOMES | SEGURO CONTINGENCIA")

| Campanha | ID | Budget/dia | Lance | CPA 16d | Leitura |
|---|---|---|---|---|---|
| `NEGATIVA VEICULAR \| BRASIL - SP \| 00` | (resolver p/ nome) | R$ 60 | Max conv · **tCPA R$ 15** | R$ 30,76 | CAMPEÃ · perde 41% por orçamento |
| `NEGATIVA VEICULAR \| SP \| 01` | (resolver p/ nome) | R$ 60 | Max conv · **tCPA R$ 15** | R$ 27,37 | forte · perde 42% por rank (teto irreal) |
| `NEGATIVA VIDA \| BRASIL - SP & MG \| 05` | (resolver p/ nome) | R$ 60 | Max conv · **SEM teto** | R$ 105,22 | SANGRANDO · CPC R$ 41 · topo abs 79% |
| `NEGATIVA SEGURO \| MG \| 04` | (resolver p/ nome) | R$ 45 | Max conv · **SEM teto** | R$ 69,65 | CPC R$ 28,82 (vs R$ 10 Inst) |
| `NEGATIVA SEGURO \| BRASIL - SP & MG \| 02` | (resolver p/ nome) | R$ 45 | Max conv · **SEM teto** | R$ 65,80 | precisa de teto |
| `NEGATIVA SEGURO \| SP \| 03` | (resolver p/ nome) | R$ 45 | Max conv · **SEM teto** | R$ 163,59 | PIOR das 2 contas |
| `NEGATIVA VIDA \| SP & MG \| 08` | (resolver p/ nome) | R$ 45 | Max conv · **SEM teto** | R$ 50,84 | precisa de teto |

- **Conversões ENABLED (confirmado API 12/06):** `CHAMADA NO WHATSAPP` (CONTACT, primary) + `Clicks to call` (CONTACT, primary, hospedada Google). Note que a Cont conta **ligação**, a Inst conta **clique no botão**: leads por ligação NÃO passam pelo WhatsApp tagueado, ficam sem código de origem.
- **Só 6 negativas** (vs 71 da Inst) — buraco grande, replicar a lista é ganho imediato sem risco (§7).
- **Total 16d (28/05-12/06):** R$ 308/dia · 93 conv · CPA médio R$ 52,96 (**1,8× a Inst**).

### Conta C — LIVRE IR · customer `3237663933`
**Fora de escopo do Seguro.** Produto descontinuado em 26/05 (memória `project_livre_ir_descontinuado`). Não incluir em relatório de Seguro salvo pedido explícito.

### GTM (2 containers — auditar os 2 sempre)
- **Inst:** `GTM-WR57KL43` (conta GTM 6210442588 · Google Ads `AW-11443839165`)
- **Cont:** `GTM-N7LKPSDN` (conta GTM 6339274960 · Google Ads `AW-17950290127`)
- Memória `project_magalhaes_gomes_gtm_containers`. Tracking corrigido em 27/05: removidas as tags PageView que inflavam conversão; conv principais hoje são WhatsApp + Form (Inst), WhatsApp + Clicks to call (Cont).

### Landing pages

**LPs atuais no ar (mapeadas por ad group via API 12/06):**

| URL atual | Conta · campanha | Estado (auditado 12/06) |
|---|---|---|
| `/seguro-negado-2/` | Cont SEGURO 02/03/04 | **SEM H1**, 180 palavras, "securitário" 0×, formulário OK, 1,25 MB |
| `/seguro-automovel-2/` | Cont VEICULAR 00/01 | H1 forte, mas 110 palavras, sem formulário, 0,96 MB |
| `/vida-negado-2/` | Cont VIDA 05/08 | **2 bugs graves:** título/H1 "Contingencia 2" vazou + botão WhatsApp aponta pro número MORTO `5531993061519` |
| `/seguro-de-vida/` | Inst VIDA 05/08 | mesmo bug do número morto `5531993061519` |
| `/seguro-carro-negado/` | Inst VEICULAR | H1 OK, raso |
| `/seguro-maquina/` | Inst NEG MÁQUINA (pausada) | — |
| `/` (home) | Inst SEGURO Geral | home genérica como LP |

**LPs novas criadas em 12/06** (pasta `clientes/magalhaes-gomes/analises/2026-06-12-otimizacao/landing-pages/`):
- `seguro-de-vida-negado.html` → destino VIDA 05/08
- `advogado-especialista-em-seguros.html` → destino SEGURO 02/03/04 (mira advogado securitário/especialista em seguros — as keywords QS 1-3)
- `seguro-veicular-negado.html` → destino VEICULAR 00/01

Cada uma: H1 casado com a keyword, casos típicos + súmulas STJ (609/616/620) + 3 passos + FAQ (~800 palavras), CSS inline leve, GTM dos 2 containers, WhatsApp `5511966629852` com código de origem por página (`[MG-VIDA]`, `[MG-SEG]`, `[MG-VEIC]`), captura de gclid/UTM em localStorage. **Pendente: publicar no domínio magalhaesgomes.com.br** (regra ONE_WEBSITE_PER_AD_GROUP — §5).

### Pipedrive — `silvapimenta.pipedrive.com` (mesma instância do Silva Pimenta)
- Funis próprios por produto: **"SEGURO"**, **"SEG VIDA"** (e "LIVRE IR" fora de escopo).
- **460 leads em 30d (jun/26) NÃO são separáveis por conta** (Inst vs Cont) no Pipedrive hoje. Trabalhar com **CPL combinado** até o tracking de origem da §11 entrar.
- Token `PIPEDRIVE_TOKEN` no `.env` central. Filtro de data em **Brasília (UTC-3)** (memória `feedback_pipedrive_timezone_brasilia`). Insights duplica atividade (bug de exibição) — usar contagem por ID distinto.
- **WhatsApp do escritório (MG):** `5511966629852` (DDD 11/SP). O antigo `5531993061519` (DDD 31) **CAIU em 27/05** — qualquer aparição dele em LP/GTM/criativo é bug a corrigir (memória `project_magalhaes_gomes_whatsapp_numero`).

---

## 4 · Benchmarks REAIS do produto (a régua de verdade)

O `benchmarks-br.md` genérico dá Financeiro CPL R$ 40-120 e CPA Search R$ 80-150 (atenção). O Seguro tem régua própria observada. Usar ESTES números pra dizer bom/ruim. **Atenção: "CPA" aqui = custo por clique-de-WhatsApp/chamada (conversão Google), não custo por lead Pipedrive.**

| Métrica | Régua real do Seguro | Leitura |
|---|---|---|
| **CPA Institucional (saudável)** | R$ 20 a 35 | patamar normal da conta com teto |
| **CPA Institucional (atenção)** | R$ 35 a 55 | investigar campanha específica |
| **CPA Contingência (meta pós-tCPA)** | igualar a Inst (R$ 25-40) | hoje está R$ 53 médio por falta de teto |
| **CPA por campanha (CAMPEÃ veicular)** | R$ 19 a 31 | escalar onde perde por orçamento |
| **CPA crítico** | > R$ 90 | zona vermelha (Cont VIDA R$ 105, Cont SEGURO SP R$ 164) |
| **CPL REAL combinado (Pipedrive)** | **R$ 74** (460 leads/30d, R$ 34.175 gasto somado, jun/26) | a verdade que importa; não separável por conta ainda |
| **CPC veicular** | R$ 4,85 (Inst 00) a R$ 10,75 (Cont) | barato, alto volume |
| **CPC seguro/vida Inst (com teto)** | R$ 7 a 15 | normal |
| **CPC seguro/vida Cont (SEM teto)** | R$ 22 a 41 | **anomalia** — alvo da §7 |
| **CTR de busca** | 9% a 16% | alto (anúncios maduros); Cont às vezes >15% |
| **Conv rate (clique→conv Google)** | 27% Inst · variável Cont | inflado pelo que "conv" significa aqui (clique) |
| **QS médio (baseline Inst 12/06)** | 1 a 4 na maioria das caras | meta: 5-6 após LPs novas |

### Distribuição que sempre vale ler
- **Device:** ~91% mobile na Inst (CPA R$ 28 vs R$ 41 desktop) · ~86% Cont. LP mobile-first absoluta.
- **Hora (Inst):** pico 9h-17h. Madrugada (23h-5h) com CPA ruim, 3h e 23h zeram conv. Madrugada some ~R$ 600/14d nas 2 contas com CPA alto.
- **Parcela perdida:** VEICULAR perde por **orçamento** (21-41%) = pode subir verba. SEGURO/VIDA Cont e SEGURO MG/SP perdem por **classificação** (32-42%) = QS + tCPA, nunca verba.

---

## 5 · As armadilhas históricas (diagnóstico diferencial)

Rodar esta lista ANTES de propor qualquer mudança. Todas já aconteceram de verdade nesta conta:

1. **Número de WhatsApp MORTO na LP (sangrando agora):** `/vida-negado-2/` (Cont) e `/seguro-de-vida/` (Inst) têm botão pro `5531993061519`, número que **caiu em 27/05**. O GTM conta a conversão, o lead nunca chega. Explica parte do CPA R$ 105 da VIDA Cont. **Conferir o número de destino de TODA LP no ar antes de qualquer análise de VIDA.** Conserto não espera teste.

2. **PageView contando como conversão (já corrigido 27/05):** antes da limpeza, o CPA da Cont parecia R$ 14-16 porque o PageView disparava como conv principal (conv rate fake de 100%). **NÃO comparar com baselines pré-27/05** — eles estão inflados. A primeira foto verdadeira é 28/05 em diante.

3. **CPC 2-4× na Contingência (distorção estrutural):** Cont sem teto de CPA compra topo absoluto a qualquer preço. NÃO é "leilão mais caro na Cont", é Smart Bidding cego. Resolve com tCPA (§7), não com pausa.

4. **tCPA R$ 15 irreal estrangulando a VEICULAR Cont:** as 2 VEICULAR da Cont TÊM teto, mas de R$ 15, enquanto o CPA real é R$ 27-31. Teto abaixo do CPA real estrangula (a 01 perde 42% por classificação). Subir pra R$ 25-28 destrava volume na campanha mais barata.

5. **Conversão = clique, NÃO lead** (igual Direito Médico): "conversões" do Google contam clique no WhatsApp / chamada, não conversa efetiva. **Nunca reportar "X conversões = X leads".** Cruzar com Pipedrive (funis SEGURO + SEG VIDA). Hoje os 460 leads/30d não são separáveis por conta — usar CPL combinado.

6. **`ONE_WEBSITE_PER_AD_GROUP`:** todos os RSAs (ENABLED **e** PAUSED) do ad group têm que apontar pro MESMO domínio raiz. As LPs novas precisam viver em `magalhaesgomes.com.br` (subpasta ou subdomínio do mesmo raiz). Trocar URL final pra outro domínio reprova o anúncio silenciosamente e mata a campanha (memória `feedback_google_ads_one_website_per_ad_group`).

7. **Vazamento de trânsito (decisão em aberto):** R$ 826/16d combinado (Inst R$ 492 · Cont R$ 332) em ~100 termos de multa/CNH/acidente de trânsito ("advogado de trânsito", "advogado de acidente de trânsito"). Convertem barato (CPA ~R$ 26 no clique) MAS quem busca isso quer multa/CNH ou processar o causador, **não defesa contra seguradora**. **NÃO negativar antes de validar qualidade no Pipedrive / com a Yasmim (SDR):** os contatos de trânsito viraram caso de seguro? Se não, negativar libera ~R$ 52/dia.

8. **Ad groups sem anúncio ativo:** 2 ad groups da Inst ("proteção veicular" e "01 | SEGURO VEICULAR NEGADO") estavam SEM nenhum RSA ENABLED em 12/06. Keyword sem anúncio não exibe. Conferir sempre `ad_group_ad.status` por ad group.

9. **145 keywords BROAD habilitadas (Inst) com R$ 0 de gasto:** não queimam dinheiro hoje, mas são porta de vazamento. A apostila manda evitar ampla — pausar em lote.

10. **Geo "Presença ou interesse":** campanhas Inst 01/03/04/08 e Cont 01/03/04/08 usam "Presença ou interesse" — por isso aparecem buscas de Fortaleza/Natal/Aracaju em campanha "SP". Como a atuação é nacional, **não é vazamento grave e cidade NÃO se negativa**; só ajustar pra "Presença" se a separação geográfica entre campanhas importar.

---

## 6 · Regras invioláveis (o que a Rita NUNCA recomenda)

- **NUNCA propor consolidar as 2 contas** (Inst + Cont). São duplicadas DE PROPÓSITO pra cobertura de leilão (memória `project_magalhaes_gomes_duas_contas_proposital`).
- **NUNCA negativar cidade** — atuação nacional (memória `feedback_nao_negativar_cidades_atuacao_nacional`). "advogado securitário sp", "seguro negado bh" = lead.
- **NUNCA negativar termo direto do produto** ("advogado securitário", "seguro de vida negado", "advogado contra seguradora", "advogado especialista em seguros"). Termo de produto que não converte se corrige por LP/RSA/QS, nunca por pausa.
- **NUNCA negativar trânsito antes de validar Pipedrive** (§5.7). É 5% do gasto e converte barato; a dúvida é qualidade, não custo. Validar com SDR antes.
- **CPL/CPA baixo NÃO é qualidade.** Cruzar com Pipedrive antes de propor escalar (memória `feedback_cpl_nao_e_qualidade`). A VEICULAR tem CPA R$ 19 mas pode trazer curioso de trânsito.
- **NUNCA pausar campanha cara que traz lead qualificado.** Otimização por QUALIDADE, não por CPL isolado (memória `feedback_otimizacao_por_qualidade_nao_cpl`).
- **Protocolo de teste: TUDO na Contingência primeiro** (decisão William 12/06, §2). Não aplicar na Inst antes da Cont validar.
- **OAB: flag SEMPRE, NÃO impõe pausa.** Toda copy/headline/LP nova lista o risco OAB explícito (sem promessa de resultado garantido, sem mercantilismo, sem captação irregular), mesmo no que o escritório mantém. William decide (memória `feedback_oab_silva_pimenta_risco_assumido`). Cuidar especialmente: "análise gratuita" em destaque é prática comum mas flagável pelo Provimento 205; "90% de aprovação" é promessa de resultado (deixar de fora de copy nova).
- **Números auditáveis do MG:** +20 anos, +15.000 processos acompanhados. **NÃO usar "90% aprovação"** em copy nova (risco OAB). Nunca inflar.
- **Ritmo híbrido:** check semanal **observa**; mudança estrutural só a cada ~14 dias pra leitura limpa de causa-efeito (memória `project_direito_medico_ritmo_hibrido`, vale aqui). Não empilhar mudança sobre mudança recente.
- **Sempre desativar Parceiros de Pesquisa e Display** em campanha Search (memória `feedback_google_ads_redes_desativar`). Hoje as 2 contas estão OK (Display/Parceiros OFF) — confirmar sempre.
- **Zero travessão** (memória `feedback_sem_travessoes`).

---

## 7 · Passada da apostila adaptada ao Seguro (ordem)

Pré-checagem do SKILL (anúncio APPROVED? conversão biddable certa? lead real no Pipedrive?) roda antes de tudo.

1. **Performance por CONTA e por CAMPANHA separadas** (CRÍTICO — não agregar as 2 contas num CPA só):
   - Tabela Inst (7 campanhas) + tabela Cont (7 campanhas), lado a lado, com budget/dia, gasto/dia, CPC, conv, CPA, lance e leitura.
   - Sempre 16d (ou janela do ciclo) × 7d.

2. **Distorção de CPC entre contas:** comparar CPC da mesma campanha nas 2 contas. Onde Cont > 1,5× Inst, sinalizar falta de teto e propor tCPA (Cont VIDA 05/08 = R$ 60 · SEGURO 02/03/04 = R$ 55 · VEICULAR 00/01 = R$ 25-28).

3. **Parcela de impressão:** ler as duas perdidas por campanha.
   - Perda por ORÇAMENTO alta (VEICULAR 21-41%) → pode subir verba SE CPA dentro da régua.
   - Perda por CLASSIFICAÇÃO alta (SEGURO/VIDA Cont, SEGURO MG/SP 32-42%) → QS + tCPA, **nunca verba**.

4. **Quality Score decomposto** (`read.py quality-scores`): separar creative / post_click (landing) / search_predicted_ctr.
   - Hoje (12/06) o componente fraco é **post_click (LP) em praticamente todas as caras**. Reportar distribuição (quantas QS 1/2/3/4/5+).
   - Keywords-âncora do problema: advogado especialista em seguros (QS 3), advogado securitário (QS 3), ações contra seguradoras (QS 2), grupo SEGURO DE VIDA NEGADO (QS 1). Meta pós-LP nova: QS 5-6.

5. **Search terms** (`read.py search-terms`, janela do relatório) cruzado com negativas existentes:
   - Termo bom não-keyword → propor adicionar (Frase/Exata) no ad group certo. Ex achados: "advogado de veículos" (CPA R$ 7,44), "advogado para processar seguradora".
   - Termo lixo → negativar a FRASE específica (cliente da seguradora, gratuito, defensoria, consórcio, emprego, app/2ª via).
   - **Trânsito:** NÃO negativar antes de validar Pipedrive (§5.7, §6).
   - **Replicar a lista de negativas da Inst (71) na Cont (6)** — ganho imediato sem risco; inclui nomes de concorrente que já pagaram clique (adriana hellering, securato, freitas advocacia).

6. **Correspondências:** frase domina (262 kw Inst). 145 BROAD habilitadas com R$ 0 (Inst) — pausar em lote. Exata com QS baixo, revisar quando LP nova subir.

7. **Lance** (§2.3): a alavanca central. Inst já tem tCPA nas SEGURO/VIDA — manter. Cont precisa de tCPA nas 5 sem teto + subir o tCPA irreal das 2 VEICULAR. Inst VEICULAR está em Maximizar Cliques com CPA campeão — **não mexer** (testar tCPA só depois do teste da Cont).

8. **Anúncios/extensões:**
   - 2 ad groups Inst SEM anúncio ativo (§5.8) — reativar/criar RSA.
   - Headlines com a keyword (reescrever os RSA dos grupos QS ≤ 4 com a keyword exata melhora relevância do anúncio).
   - Extensões: Cont tem só 4 callouts vs 10 da Inst. Replicar callouts + snippet (até +15% CTR de graça, melhora o componente CTR esperado do QS).

9. **Higiene:** Display OFF, Parceiros OFF (as 2 contas OK em 12/06, confirmar). Geo "Presença" vs "Presença ou interesse" (§5.10).

10. **Device + hora** (se volume permitir): mobile dominante; madrugada 23h-5h com CPA ruim (excluir bloco via ad schedule é ajuste fino opcional, ganho modesto).

---

## 8 · Checklist cirúrgico — o que olhar em TODO relatório de Seguro

- [ ] **Pré-checagem do SKILL** (anúncio APPROVED? conversão biddable certa? número WhatsApp da LP VIVO?) ANTES de qualquer métrica.
- [ ] **Conferir número de WhatsApp das LPs no ar** (bug do `5531993061519` morto — §5.1).
- [ ] **Performance separada por CONTA (Inst × Cont) e por campanha** — nunca um CPA combinado só.
- [ ] **Distorção de CPC entre contas** medida (mesma campanha, Cont vs Inst).
- [ ] **Lead REAL no Pipedrive** (funis SEGURO + SEG VIDA), não só "conversions" do Google. CPL combinado (não separável por conta ainda).
- [ ] **QS decomposto** mostrando LP como gargalo (post_click BELOW_AVERAGE nas caras).
- [ ] **Parcela perdida:** orçamento (VEICULAR, pode verba) vs classificação (SEGURO/VIDA Cont, QS+tCPA).
- [ ] **Lance por campanha:** quais Cont estão SEM teto (sangrando)? VEICULAR Cont com tCPA irreal R$ 15?
- [ ] **Negativas Cont (6) vs Inst (71)** — replicar.
- [ ] **Search terms:** convertedores não-keyword (adicionar) e lixo (negativar dentro das regras §6). Trânsito só com validação Pipedrive.
- [ ] **Status das 3 LPs novas:** publicadas? URL final dos ad groups da Cont apontada? GTM dispara no botão novo?
- [ ] **Protocolo de teste respeitado:** mudança só na Cont nesta fase?
- [ ] **Tendência (ciclo atual vs anterior)** narrada; lembrar que pré-27/05 está inflado por PageView.
- [ ] **Flag OAB** nas peças/extensões/LPs ("análise gratuita", sem "90%", sem promessa).

---

## 9 · Estrutura do relatório de Seguro (HTML cirúrgico)

Seguir o modelo da Rita, com estas seções específicas. **Paleta Magalhães Gomes (NÃO a teal do Silva Pimenta):** marrom-noite `#3E2818` / `#181410` · bronze `#CCA24E` · lacre `#B3422E` · creme `#F7F2E9`. Fontes Fraunces (display) + Archivo (corpo). Logo dourado do MG.

1. **KPIs topo:** gasto combinado · conv combinada · **CPA Inst e CPA Cont separados** · CPL real Pipedrive (combinado) · QS médio. Sempre 16d × 7d.
2. **Resumo executivo:** 3-5 bullets do que mais importa (distorção CPC, VEICULAR estrangulada, vazamento trânsito, QS/LP).
3. **Performance por conta** (2 tabelas, Inst × Cont lado a lado) — a seção central. Pills coloridas por leitura (campeã/cara/sangrando).
4. **Distorção CPC entre contas** (tabela mesma campanha Inst vs Cont, multiplicador).
5. **Parcela de impressão:** gargalo por campanha (orçamento vs classificação), 2 colunas.
6. **Lance:** atual vs proposto (tabela com tCPA por campanha da Cont).
7. **Quality Score decomposto:** top keywords × QS × componente fraco × ação. Mostra LP como gargalo.
8. **Search terms:** convertedores (adicionar) + lixo (negativar) com **botão copiar** nas negativas. Box separado pro trânsito (decisão pendente).
9. **Negativas Cont vs Inst:** lista a replicar com botão copiar.
10. **LPs:** status das 3 novas + bug do número morto + plano de publicação.
11. **Tracking de fechamento (§11):** status do projeto gclid → Pipedrive → conversão offline.
12. **Plano 3 camadas:** HOJE (negativas, número morto, RSA morto) · ESTA SEMANA (tCPA, realocação na Cont) · 2 SEMANAS (LP no ar, replicar Inst se Cont melhorou).
13. **Compliance OAB** + audit log + próximo ciclo + footer.

**Onde salvar (padrão MG, NÃO o caminho do Silva Pimenta):** pasta datada `clientes/magalhaes-gomes/analises/YYYY-MM-DD/` com `INDEX.html` navegável + `analises/01-google-ads.html` (Inst+Cont) + `dados/` (todos os JSONs da API + scripts de análise + audit log). Entrega antiga é histórico, **não regerar** — pasta nova por data (memória `feedback_propostas_relatorios_historico`).

> Referência viva de relatório bem feito: `clientes/magalhaes-gomes/analises/2026-06-12-otimizacao/INDEX.html` (este foi o que originou este playbook). Diagnóstico anterior das 2 contas: `2026-05-27-diagnostico-geral/`.

---

## 10 · Comandos de API prontos (copy-paste, rodar da raiz do workspace)

```bash
INST=1301598996    # Institucional
CONT=2903149800    # Seguro Contingência

# Métricas por campanha (rodar nas 2 contas; janela limpa pós-27/05)
python .claude/skills/google-ads-ratos/scripts/read.py campaigns --customer-id $CONT --since 2026-05-28 --until 2026-06-12
python .claude/skills/google-ads-ratos/scripts/read.py campaigns --customer-id $CONT --date-range LAST_7_DAYS

# Search terms (limite alto — 100 default corta) + negativas atuais
python .claude/skills/google-ads-ratos/scripts/read.py search-terms --customer-id $CONT --since 2026-05-28 --until 2026-06-12 --limit 3000
python .claude/skills/google-ads-ratos/scripts/read.py negative-keywords --customer-id $CONT

# Quality Score decomposto (limite alto)
python .claude/skills/google-ads-ratos/scripts/read.py quality-scores --customer-id $CONT --limit 1000

# Keywords + match type + métricas; Ad groups; Anúncios (RSA, p/ ver final_urls e status); Extensões
python .claude/skills/google-ads-ratos/scripts/read.py keywords --customer-id $CONT --since 2026-05-28 --until 2026-06-12
python .claude/skills/google-ads-ratos/scripts/read.py ad-groups --customer-id $CONT
python .claude/skills/google-ads-ratos/scripts/read.py ads --customer-id $CONT --since 2026-05-28 --until 2026-06-12
python .claude/skills/google-ads-ratos/scripts/read.py extensions --customer-id $CONT

# Insights: parcela de impressão por campanha + device + hora + diário
python .claude/skills/google-ads-ratos/scripts/insights.py campaign --customer-id $CONT --since 2026-05-28 --until 2026-06-12
python .claude/skills/google-ads-ratos/scripts/insights.py device --customer-id $CONT --date-range LAST_14_DAYS
python .claude/skills/google-ads-ratos/scripts/insights.py hourly --customer-id $CONT --date-range LAST_14_DAYS
python .claude/skills/google-ads-ratos/scripts/insights.py daily  --customer-id $CONT --date-range LAST_30_DAYS
```

**GAQL custom** (via `lib.run_query`) pro que o `read.py` não cobre — usado no relatório de 12/06:
- Parcela perdida + lance + redes + geo por campanha:
  `SELECT campaign.name, campaign.bidding_strategy_type, campaign.network_settings.target_content_network, campaign.network_settings.target_partner_search_network, campaign.geo_target_type_setting.positive_geo_target_type, metrics.search_impression_share, metrics.search_budget_lost_impression_share, metrics.search_rank_lost_impression_share, metrics.search_top_impression_share, metrics.search_absolute_top_impression_share FROM campaign WHERE segments.date BETWEEN ... AND campaign.status='ENABLED' AND metrics.impressions>0`
- tCPA atual: `campaign.maximize_conversions.target_cpa_micros` / `campaign.target_cpa.target_cpa_micros`
- Auto-tagging + conversões: `SELECT customer.auto_tagging_enabled FROM customer` · `SELECT conversion_action.name, conversion_action.category, conversion_action.primary_for_goal FROM conversion_action WHERE conversion_action.status='ENABLED'`
- Status de aprovação do anúncio (pré-checagem): `SELECT ad_group_ad.policy_summary.approval_status FROM ad_group_ad`

**Auditoria de LP ao vivo** (peso, tempo, número de WhatsApp, conteúdo) — Playwright headless, mobile UA. Script de referência: `clientes/magalhaes-gomes/analises/2026-06-12-otimizacao/dados/audit-site.js`. O site bloqueia WebFetch (403); usar `curl.exe -A "Mozilla/5.0..."` ou Playwright com user agent de navegador.

**Encoding Windows:** as saídas têm acentos das keywords que quebram cp1252. Ler JSON com `encoding='cp1252'` ou `errors='replace'`, e prefixar `PYTHONIOENCODING=utf-8` no parse. Redirecionar stderr (`2>nul` no cmd) — o script loga no stderr e o exit code pode aparecer 255 mesmo com JSON válido.

**Aplicar mudanças (via API, com aprovação do William, status conservador):**
```bash
# Replicar negativa na Cont (frase)
python .claude/skills/google-ads-ratos/scripts/create.py negative --customer-id $CONT --campaign-id <ID> --text "seguro de carro" --match-type PHRASE
# Adicionar keyword nova
python .claude/skills/google-ads-ratos/scripts/create.py keyword  --customer-id $CONT --ad-group-id <ID> --text "advogado de veículos" --match-type PHRASE
# tCPA / budget via update.py (validate_only ANTES). Orçamento Google em MICROS (R$50 = 50.000.000).
```

**Atenção:** orçamento Google em **MICROS** (R$ 50 = 50.000.000), diferente do Meta (centavos). `LAST_2_DAYS` não existe no GAQL — usar datas absolutas. Sempre `validate_only` antes de mutate real.

---

## 11 · Tracking de fechamento (gclid → Pipedrive → Conversão Offline)

Projeto desenhado em 12/06 pra responder "qual campanha fechou contrato". Estado e plano (relatório deve registrar o avanço):

- **Pré-condição OK:** auto-tagging (gclid) **ATIVO nas 2 contas** (confirmado API). Todo clique chega na LP com gclid.
- **Nível 1 — tag no Pipedrive:** LP injeta código de origem no botão WhatsApp (`[MG-VEIC]`, `[MG-SEG]`, `[MG-VIDA]` — já nas LPs novas) + captura gclid/UTM em localStorage. Clonar o cenário Make "Tag Lead" do Silva Pimenta pro Digisac do MG (`magalhaesgomes.digisac.me`) — pendência JÁ mapeada no cartão 01 das automações do SP. Deal nasce no funil certo com campanha + origem.
- **Nível 2 — Conversão Offline (o ouro):** quando o deal vira `won`, script diário pega o gclid e sobe conversão "FECHAMENTO DE CONTRATO" via API na conta certa (gclid aceita até 90 dias). Aí o Google mostra fechamento por campanha/keyword e o Smart Bidding pode otimizar por contrato, não por clique. Resolve de vez a dúvida do trânsito (§5.7).
- **Limitações honestas:** leads por LIGAÇÃO (Clicks to call da Cont) não passam pelo WhatsApp, ficam sem código; ~9% dos leads apagam o texto pré-preenchido (cai em "origem a confirmar"); não é retroativo (começa do dia que ligar).
- **Roadmap-mãe:** `clientes/silva-pimenta/dashboard-financeiro/utm-tracking-roadmap.md` (cartão 14). Construindo pro MG primeiro, o mesmo motor serve depois pro médico no Google.

---

## 12 · Decisões já tomadas (não relitigar)

- **2 contas duplicadas DE PROPÓSITO** (cobertura de leilão). Nunca consolidar (William 27/05).
- **Tracking corrigido em 27/05:** PageView removida dos 2 GTMs e arquivada no Ads. Conv principais hoje: WhatsApp + Form (Inst), WhatsApp + Clicks to call (Cont). Baselines pré-27/05 estão inflados.
- **NEG MÁQUINA pausada** por baixo volume (William 27/05). Não reativar sem decisão.
- **WhatsApp MG = `5511966629852`** (DDD 11). O `5531993061519` (DDD 31) caiu em 27/05 — bug onde aparecer.
- **Protocolo de teste: tudo na Contingência primeiro, LPs antes das ações** (William 12/06). Replicar na Inst só se a Cont melhorar.
- **3 LPs novas criadas em 12/06** (vida-negado, especialista-seguros, veicular-negado) — pendentes de publicação no `magalhaesgomes.com.br`.
- **LIVRE-IR descontinuado** (26/05) — conta `3237663933` fora do escopo de Seguro.
- **Plano de não-mexer foi de 27/05 a 10/06** (calibração Smart Bidding pós-tracking). A partir de 12/06 a janela limpa permite agir.

---

## 13 · Critério de sucesso (confere ANTES de entregar)

Se faltar 1 item, NÃO entrega, completa primeiro.

- [ ] **Pré-checagem do SKILL rodada** (anúncio APPROVED? conversão biddable certa? número WhatsApp da LP vivo?) ANTES de qualquer métrica.
- [ ] **Performance separada por CONTA (Inst × Cont) e por campanha** — nunca CPA combinado único.
- [ ] **Distorção de CPC entre contas medida** e tCPA proposto onde Cont sangra.
- [ ] **Lead REAL no Pipedrive** (funis SEGURO + SEG VIDA), CPL combinado, não só "conversions" Google.
- [ ] **Janela limpa pós-27/05** (não comparar com baseline inflado por PageView).
- [ ] **30/16/7 (ou ciclo) puxados da API**, não estimados. CPA contra a régua REAL (Inst R$ 20-35), não o genérico.
- [ ] **QS decomposto** mostrando LP (post_click) como gargalo nas caras.
- [ ] **Parcela perdida** classificação vs orçamento por campanha (VEICULAR = verba; SEGURO/VIDA Cont = QS+tCPA).
- [ ] **Negativas Cont (6) vs Inst (71)** sinalizadas pra replicar.
- [ ] **Nenhuma negativa de cidade, de termo de produto, nem de trânsito sem validação Pipedrive.**
- [ ] **Nenhuma proposta de consolidar as 2 contas.**
- [ ] **Status das 3 LPs novas + bug do número morto** registrados.
- [ ] **Protocolo de teste respeitado** (mudança só na Cont nesta fase).
- [ ] **Plano 3 camadas + flag OAB** (sem impor pausa, sem "90%", "análise gratuita" flagada). Zero travessão.
- [ ] **Dashboard HTML datado** na pasta `clientes/magalhaes-gomes/analises/YYYY-MM-DD/` com `INDEX.html` + `analises/` + `dados/`. Paleta marrom-bronze MG.
- [ ] **Status PAUSED / validate_only** em qualquer ação via API. **Pergunta antes de executar mudança real.**
- [ ] **Entrada no `clientes/magalhaes-gomes/_contexto/atividades-recentes.md`** via `/fechar-sessao` no fim.
```
