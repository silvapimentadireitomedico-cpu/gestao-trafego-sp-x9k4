# Rita-nuvem — relatório diário automático

Entrega o relatório da Rita todo dia de manhã (WhatsApp + Discord, link às 8h) sem
depender da máquina do William. Tudo roda no GitHub Actions deste repo, que já tem os
tokens de ads como secrets.

## Arquitetura (decidida 19/06/2026)

```
GitHub Action (cron 07:50 BRT)  .github/workflows/rita.yml
  1. scripts/rita_collector.py   -> data/rita/<produto>.json   (dump granular, 30/14/7d)
  2. scripts/gerar_relatorio_rita.py --auto
        le data/rita/<produto-do-dia>.json + rita/SKILL.md + reference do produto
        chama a API Anthropic (claude-opus-4-8)  -> relatorios/rita-<produto>-<data>.html
  3. commita data/rita + relatorios
  4. scripts/notificar_rita.py "<resumo>" "<link>"   (WhatsApp CallMeBot + Discord)
```

A Rita é **read-only**: a única fonte é o JSON dumpado. Ela NÃO toca a API de ads.
Nenhum token de ads é copiado pra lugar novo (a Action já os tinha).

Cadência (BRT): **seg** Auxílio Moradia · **ter** FIES · **qua** Seguro · **qui** Direito Médico.
Sexta/fim de semana: o dump roda, o relatório não (no-op).

## Ativar (uma vez)

1. **Adicionar os secrets novos** em Settings > Secrets and variables > Actions:
   - `ANTHROPIC_API_KEY` — chave da API Anthropic (gera o relatório; ~US$ 1/relatório, 1/dia).
   - `DISCORD_WEBHOOK_AUTOMACOES` — webhook do canal #automações (valor no `.env` raiz do workspace).
   - `WHATSAPP_CALLMEBOT_PHONE` — `553182248808`.
   - `WHATSAPP_CALLMEBOT_APIKEY` — `5198836`.
   (Os secrets de ads — Google/Meta/Pipedrive — já existem, são os mesmos do dashboard.)
2. **(Opcional) Variable `RITA_PAGES_BASE`** se o link público não for o github.io padrão
   (`https://silvapimentadireitomedico-cpu.github.io/gestao-trafego-sp-x9k4`).
3. **Conferir GitHub Pages** ligado (Settings > Pages > main / root) pra o link abrir.

## Testar antes de confiar no agendamento

- **Sem custo de API:** `python scripts/rita_collector.py direito-medico` (dump real) e
  `python scripts/gerar_relatorio_rita.py direito-medico --dry-run` (monta o prompt, não chama a API).
- **De ponta a ponta:** Actions > "Rita - relatorio diario" > Run workflow, escolhendo um
  produto no input (ex: `direito-medico`). Confere o HTML em `relatorios/` e o aviso no WhatsApp/Discord.
  Só depois disso confiar no cron das 07:50.

## Lacunas v1 (a Rita reporta como pendência no próprio relatório)

- Quebra de perdas por "número da campanha" (campo da pessoa no Pipedrive) — cruzamento
  ainda calibrando pós-16/06.
- Checagem de WhatsApp vivo na LP (gate 2 de tracking) — exige ler a LP, fora do JSON.
