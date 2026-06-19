# Playbook Rita · DIREITO MÉDICO (Silva Pimenta)

> **LER ANTES de qualquer relatório/otimização de Direito Médico.** Este arquivo é a inteligência específica do produto: contas, funil, régua real, armadilhas já vividas e regras invioláveis. O Gabarito ADAPTA e as skills de análise continuam valendo por cima disto. Última calibragem: 12/06/2026.
> **Verificação em cadeia:** os IDs abaixo foram lidos da API em 12/06. Campanha pode ser excluída/recriada (já aconteceu) — sempre **resolver por NOME** e confirmar o ID na hora; tratar os IDs daqui como atalho, não como verdade eterna.

---

## 1 · O produto em 30 segundos

- **Quem é o lead:** médico (28-55) que **já tem um problema acontecendo** — foi intimado pelo CRM (sindicância), responde a processo ético (PEP), foi acusado de erro médico ou é réu em ação judicial. É dor aguda, urgência real, alto valor de contrato.
- **REGRA DE OURO:** o escritório **só defende o MÉDICO**, nunca o paciente. Tudo que cheira a "paciente querendo processar médico" é lixo a cortar, não lead.
- **Atuação NACIONAL.** Nunca tratar cidade no termo como desqualificação.
- **Canal histórico:** Google Search (demanda declarada, finita). **Meta entrou em jun/2026** como alavanca de volume (demanda gerada). Os dois rodam juntos hoje.
- **Meta de operação (jun/2026):** ritmo de **50 leads/mês**. Projeção honesta: Google entrega 25-40 (teto da demanda), o Meta é quem cruza os 50.

---

## 2 · Mapa de contas e IDs (puxar sem perguntar)

### Google Ads — customer `6351554556`
| Campanha | ID | Papel |
|---|---|---|
| `[PESQUISA] DIREITO MEDICO \| BRASIL - SP` | `23646069979` | Principal (termos cabeça + erro médico) → LP `/` e `/erro-medico` |
| `[PESQUISA] DIREITO MEDICO \| SP` | `23669965564` | Principal recorte SP |
| `[PESQUISA] DM \| SINDICANCIA & PROCESSO ETICO` | `23932333103` | Nova 11/06 → LPs `/sindicancia-crm` e `/processo-etico` |
| `[PESQUISA] DM \| DEFESA JUDICIAL` | `23932333349` | Nova 11/06 → LP `/defesa-judicial` |

- **Conversão que importa:** `BOTÃO WHATSAPP | DIREITO MÉDICO` (id `7528943403` · tag `AW-16456666854/xtjYCKueioYcEOadk6c9`). Conta tanto clique no botão WhatsApp quanto envio de formulário (mesmo label). **Conta o CLIQUE/intenção, não a conversa efetiva** (ver §3).
- **PageView** (`AW-16456666854/DRujCMqN94UcEOadk6c9`) é secundária. Não tratar como lead.
- **Checagem técnica (igual AM):** o que guia o Smart Bidding é `campaign_conversion_goal.biddable`, NÃO o `primary_for_goal` (legacy, retorna OK fantasma no mutate). Se a LP mudar e o goal biddable continuar apontando pra conversão que a página não dispara mais, o bidding fica cego (CPC explode, CTR cai, 0 conversão). Validar sempre que a conversão biddable = a que a LP dispara hoje.
- **Lista de negativas compartilhada:** `Negativas | Direito Médico` (id `10957938966`, ~295 termos após limpeza de 12/06). Aplicada SÓ nas 2 principais. **NÃO está nas campanhas novas** (decisão em aberto: aplicar na Judicial sim; na Sindicância não, porque "o que é", "prazo", "suspensão" são avatar qualificado lá).

### Meta Ads — conta `act_320965166251046` (SP Brasil, BRL) · Página `122709140730544`
| Campanha | ID | Status |
|---|---|---|
| `[META] DIREITO MEDICO \| CTWA \| 2026-06` | `120248977689170439` | **ATIVA** (formato vencedor) |
| `[META] DIREITO MEDICO \| WhatsApp \| 2026-06` | `120248911825280439` | PAUSADA (formato tráfego, abandonado — ver §5) |

- **Conjuntos:** `DM-80` Base de clientes R$20/d · `DM-81` LAL 1% R$30/d (base excluída). Otimização **CONVERSATIONS**, destino WhatsApp, **mobile-only**, posicionamentos FB+IG feed/stories/reels.
- **Públicos:** Base clientes `120248908455920439` · LAL 1% `120248908470740439` · LAL 3% `120248908472160439` (reserva de escala). Base = 1.697 contratos GANHOS do Pipedrive (FIES+AM+DM), hasheada.
- **Destino WhatsApp:** o CTWA usa o número conectado à Página. **(11) 97716-7482 voltou do ban em 12/06** e é o destino atual; plano futuro é um número por produto (exige números na API oficial do WhatsApp na BM).

### Pipedrive — `silvapimenta.pipedrive.com`
- **Funil Direito Médico:** pipeline `6`, stage inicial `46`. Dono: **Rodrigo Hurtado** (`26103112`).
- **Sem Funil** (onde caem leads sem código): pipeline `5`, stage `44`.
- **Campos:** NÚMERO DA CAMPANHA `4b3b309495d5824b2324298d7314d500dda69f61` · ORIGEM `e4efa4f675f4d15498435e678eb01a6fcabaeb3b` (enum: 61=Google Ads, 59=Meta Ads).
- Token em `.env` central (`PIPEDRIVE_TOKEN`). Filtros de data em **Brasília (UTC-3)**.

---

## 3 · O funil de conversão (e por que a contagem mente)

```
Anúncio → clique → WhatsApp abre com mensagem tagueada → pessoa ENVIA → cai no WhatsApp do escritório (Digisac) → Make tagueia no Pipedrive
```

**A regra de leitura mais importante do produto:** a "conversão" do Google/Meta conta o **clique/intenção**, não a mensagem enviada. Entre clique e conversa real há perda. **Nunca reportar "X conversões = X leads".** Sempre cruzar:
- **Google/Meta** = quantos clicaram (topo).
- **Pipedrive** = quantos viraram conversa real (fundo). Esta é a verdade que importa.

**Onde o lead de verdade aparece:**
- **Com código** (`. 80`/`. 81` no Meta; `DM-GERAL/DM-ERRO/DM-SIND/DM-PROC/DM-JUD` no Google): o Make cria pessoa+deal no funil **Direito Médico (6)** com ORIGEM e dono Rodrigo. Procurar por NÚMERO DA CAMPANHA e ORIGEM.
- **SEM código** (template apagado OU **falha de criptografia do WhatsApp**, comum em conexão QR): cai em **Sem Funil (5)** com título `(ORIGEM A CONFIRMAR)`. **SEMPRE varrer o Sem Funil** na janela do relatório — tem lead de DM escondido lá. Não está taggeado ≠ não existe.

**Implicação pro relatório:** se o Google/Meta mostram cliques mas o Pipedrive (funil DM + Sem Funil) está vazio na mesma janela, **isso é vazamento, não baixa demanda** — investigar §5 antes de qualquer corte.

---

## 4 · Benchmarks REAIS do produto (a régua de verdade)

Os benchmarks-br genéricos servem de piso, mas o DM tem régua própria observada na conta. Usar ESTES números pra dizer "bom/ruim":

| Métrica | Régua real do DM | Leitura |
|---|---|---|
| **CPL Google (histórico)** | ~R$ 180 | patamar normal; abaixo é ótimo, muito acima investiga LP/QS |
| **CPC termo cabeça** ("advogado direito médico") | R$ 6 a 23 · concorrência HIGH | caro por natureza; não dá pra "baratear no grito" |
| **CPC sindicância / processo ético** | R$ 2 a 8 · concorrência LOW | a oportunidade barata do produto |
| **QS médio (baseline 11/06)** | 4,8 · página "abaixo da média" em 12/12 | meta do William: chegar a 8; reage lento por volume baixo |
| **Parcela perdida por classificação** | 44-77% | gargalo é AdRank/QS, **não orçamento** (perda por orçamento ~7-19%) |
| **Demanda total do nicho** | ~1.100-1.300 buscas exatas/mês (Brasil, todos os temas) | Google é teto finito; "advogado direito medico" = 720/mês, "sindicancia crm" = 170/mês, judicial ~30-50/mês |
| **Device** | ~71% mobile | WhatsApp é mobile; desktop converte pior no clique-pra-conversa |

**Não confundir:** parcela perdida por classificação alta NÃO se resolve com mais orçamento (erro clássico). Resolve com QS (LP + relevância + CTR). Aumentar verba só paga mais caro pra seguir mal posicionado.

---

## 5 · As 6 armadilhas históricas (diagnóstico diferencial)

Quando o relatório mostrar "cliques sem lead", rodar esta lista ANTES de culpar a demanda. Todas já aconteceram de verdade:

1. **Popup-blocker do webview (mobile):** botão WhatsApp via `window.open()` é bloqueado no navegador interno do app → conversão conta, WhatsApp não abre. **Fix aplicado:** link nativo no `href`. Se reaparecer cliques-sem-conversa, conferir se algum botão voltou a usar JS.
2. **Mensagem pré-preenchida ruim:** URL gigante ("Vim da página: https://...") parece spam + acento mal codificado bugava o texto → ninguém envia. **Fix:** mensagem curta, natural, `encodeURIComponent`.
3. **Formato Meta errado:** campanha de **tráfego** (otimiza por clique) traz curioso. O que funciona na casa é **CTWA / OUTCOME_ENGAGEMENT / CONVERSATIONS** (igual FIES). Se virem campanha DM de tráfego ativa, é a errada.
4. **Número de WhatsApp caído:** o destino já caiu uma vez (7482 banido em 03/06 → migrou pro 8618 → 7482 voltou em 12/06). Cliques sem nenhuma conversa pode ser número morto. Conferir o número ativo no destino e se está sendo atendido.
5. **Falha de criptografia do Digisac (QR):** mensagens chegam como placeholder e o lead cai em Sem Funil sem código. Não é perda — é busca no lugar errado. Varrer Sem Funil.
6. **QS travado + página "abaixo":** a página já é rápida (Cloudflare). O componente "experiência" reage por **volume de cliques + sinal de conversão**, e só recomeçou a contar quando os fixes de conversão entraram (08-12/06). Esperar é correto; alarmar QS baixo na 1ª semana não.

---

## 6 · Regras invioláveis (o que a Rita NUNCA recomenda)

- **Nunca negativar cidade** (atuação nacional). "advogado direito médico curitiba" = lead, não lixo.
- **Nunca negativar termo do próprio produto** ("advogado direito médico", "defesa médica", "sindicância"). Termo de produto que não converte se corrige por LP/RSA/QS, não por pausa.
- **Sindicância: NÃO negativar "o que é / prazo / suspensão / consulta"** — é o médico em pânico recém-intimado, o avatar mais quente.
- **Blindagem anti-paciente é obrigatória** na Judicial e Erro Médico: negativas como "como processar", "indenização", "vítima", "direitos do paciente", "contra médico". Se faltar, sinalizar.
- **Otimização por QUALIDADE, não por CPL:** não pausar campanha cara que traz lead/venda qualificada. Decidir por vendas + tags Pipedrive. CPL isolado engana.
- **Ritmo híbrido:** check **observa**; mudança estrutural só a cada ~14 dias, pra leitura limpa de causa-efeito. Não empilhar mudança sobre mudança recente.
- **Compliance OAB:** flag sempre (sem promessa de resultado, sem mercantilismo, sem captação irregular), mesmo no que o escritório optou por manter. Flaggar ≠ impor pausa (William decide; performance > compliance estrita é decisão consciente dele).
- **Zero travessão.**

---

## 7 · Passada da apostila adaptada ao DM (ordem)

1. **Termos de pesquisa** (`search-terms`, janela do relatório) cruzado com as negativas existentes: termo bom não-keyword → propor adicionar; termo lixo → negativar a **frase específica** (ex: "processar cirurgião"), nunca o termo solto que também é do médico. Cuidar das regras §6.
2. **Quality Score decomposto** (`keywords`): separar "anúncio" / "página" / "CTR esperada". Hoje o gargalo é página (volume) + CTR. Reportar QS médio e a tendência vs baseline 4,8.
3. **Parcela de impressão:** ler as duas perdidas. Classificação alta = QS/AdRank (NÃO mexer orçamento). Orçamento alto = aí sim avaliar verba, se CPL/qualidade permitirem.
4. **Correspondências:** frase/exata preferidas; ampla só com negativa forte.
5. **Lance:** com histórico de conversão (DM tem ~23 conv/30d), avaliar **Maximizar Conversões**. Migrar só com dado limpo (não sobre estrutura recém-mexida).
6. **Anúncios/extensões:** RSA com keyword no título; sitelinks/callouts ativos.
7. **Higiene:** Parceiros de Pesquisa e Display OFF (sempre conferir — create.py vem com Parceiros ON).

---

## 8 · Checklist cirúrgico — o que olhar em TODO relatório de DM

- [ ] **Pipedrive primeiro:** quantos deals novos no funil DM (6) + quantos `(ORIGEM A CONFIRMAR)` no Sem Funil (5) na janela. Esse é o número de lead REAL.
- [ ] **Cruzar** com conversões Google + conversas Meta. Gap grande = rodar §5 (vazamento), não cortar verba.
- [ ] **Google:** termos novos (lixo? adicionar?), QS vs 4,8, parcela perdida (classificação vs orçamento), CPL por campanha (principal vs sindicância vs judicial — comparar os 3 do desmembramento).
- [ ] **Meta:** está no formato CTWA? frequência por conjunto (Base é pequena, satura rápido — frequência >3-4 vira alerta), CTR, custo por conversa, aprendizado saiu de "learning"?
- [ ] **Device/hora** se o volume permitir.
- [ ] **Tendência 30→14→7** pra separar causa de efeito.
- [ ] **Flag OAB** nas peças/extensões.

---

## 9 · Estrutura do relatório de DM (HTML cirúrgico)

Seguir o modelo da Rita (`dashboard-orcamento/relatorios/`), com estas seções específicas do produto, **Google e Meta separados**:
1. **KPIs topo:** leads REAIS (Pipedrive) · conversões Google · conversas Meta · CPL real · gasto total · QS médio.
2. **Funil de verdade:** clique → conversa → lead Pipedrive (mostrar a perda em cada etapa; é a narrativa central do produto).
3. **Google por campanha** (as 3 + recorte SP): impressões, CPC, CPL, QS, parcela perdida. Termos novos com botão copiar nas negativas a aplicar.
4. **Meta por conjunto:** Base vs LAL, frequência, custo/conversa, criativo vencedor.
5. **Bom / Ruim / Recomendações pra aprovar** (3 camadas: hoje / semana / 2 semanas).
6. **Pendências e decisões em aberto.**

**Onde salvar (padrão da casa, igual AM, NÃO em `relatorios/`):** pasta datada `clientes/silva-pimenta/marketing/trafego-pago/otimizacoes/direito-medico/YYYY-MM-DD/` com `INDEX.html` navegável + `analises/01-google-ads.html` + `analises/02-meta-ads.html`. Paleta da marca (teal `#1A4758` + champagne `#C5A57A`). Sempre **14d vs 7d** + botão copiar nas negativas. Entrega antiga é histórico, **não regerar** — pasta nova por data.

---

## 12 · Comandos de API prontos (copy-paste, rodar da raiz do workspace)

```bash
CID=6351554556   # Google Ads Direito Médico

# Métricas por campanha (rodar LAST_30_DAYS / 14 / 7)
python .claude/skills/google-ads-ratos/scripts/read.py campaigns --customer-id $CID
# Termos de pesquisa (desperdício)
python .claude/skills/google-ads-ratos/scripts/read.py search-terms --customer-id $CID
# Quality Score decomposto
python .claude/skills/google-ads-ratos/scripts/read.py quality-scores --customer-id $CID
# Device / hora / dia
python .claude/skills/google-ads-ratos/scripts/insights.py account --customer-id $CID --date-range LAST_7_DAYS

# Meta (CTWA): conta act_320965166251046, token META_ADS_TOKEN
python .claude/skills/meta-ads-ratos/scripts/read.py campaigns --account act_320965166251046
```

GAQL custom (via `lib.run_query`) pro que o read.py não cobre: status de aprovação do anúncio (`ad_group_ad.policy_summary.approval_status` — pré-checagem do SKILL), `campaign_conversion_goal.biddable`, `conversion_action` + tag_snippets (achar o label), histórico diário (`segments.date`), parcela de impressão por keyword (atenção: `search_budget_lost_impression_share` NÃO é válido em `keyword_view`). `LAST_2_DAYS` não existe no GAQL — usar datas absolutas. Orçamento Google em **MICROS** (R$50 = 50.000.000); Meta em **CENTAVOS** (R$50 = 5000).

**Pipedrive (lead real):** token `PIPEDRIVE_TOKEN` no `.env`. Leads do funil DM = pipeline 6; varrer também Sem Funil (pipeline 5) por `(ORIGEM A CONFIRMAR)`. Filtro de data em Brasília (UTC-3).

---

## 13 · Critério de sucesso (confere ANTES de entregar)

- [ ] **Pré-checagem do SKILL rodada** (anúncio APPROVED? conversão biddable certa? lead real no Pipedrive?) ANTES de qualquer métrica.
- [ ] **Lead REAL contado no Pipedrive** (funil DM 6 + Sem Funil 5 `ORIGEM A CONFIRMAR`), não só "conversions" do Google/Meta.
- [ ] Gap clique→conversa investigado pela §5 antes de qualquer corte de verba.
- [ ] 30/14/7 puxados da API; CPL comparado à régua REAL (~R$180), não ao genérico.
- [ ] QS vs baseline 4,8; parcela perdida classificação vs orçamento (não subir verba se for classificação).
- [ ] Meta no formato CTWA; frequência por conjunto (Base satura rápido).
- [ ] Nenhuma negativa de cidade nem de termo de produto; anti-paciente presente na Judicial/Erro.
- [ ] Plano em 3 camadas + flag OAB. Zero travessão. Dashboard datado na pasta certa.

---

## 10 · Decisões já tomadas (não relitigar)

- Desmembramento em 3 campanhas Google: **decisão da diretoria**, validada por volume.
- LP nova `/defesa-judicial` criada no padrão das 5; pixel Meta `278021291688313` em todas as LPs (eventos Contact no clique, Lead no form).
- Formato Meta = CTWA (tráfego foi testado e abandonado).
- Base de clientes + LAL 1% autorizados pelo William (LAL é exceção à regra de "público puro" — ele aprovou explicitamente pra esse produto).
- Lista compartilhada limpa em 12/06 (removidos: cidades, "saude", "penal", "atestado", "suspensão", "prazo", "consulta", "iatrogenia", "sigilo" e duvidosas cirurgia/parto/morte/prescrição/residente/sus — destravavam médico qualificado).

---

## 11 · Cadência e datas-âncora

- **Quinta = dia de Direito Médico** (cadência semanal da Rita).
- Baseline QS **4,8 em 11/06** (comparar sempre contra isto).
- Mudanças estruturais grandes: 29/05 (URLs+QS), 03/06 (WhatsApp direto), 08/06 (mensagem), 11/06 (desmembramento+Meta), 12/06 (CTWA+limpeza negativas). Ler efeito 3-14 dias depois de cada.
- Tags do Pipedrive maduras ~16/06 em diante; antes disso, sinalizar que a leitura de qualidade ainda calibra.
