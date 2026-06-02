#!/usr/bin/env python3
"""Soma o CSV do Pipedrive Insights e compara com o que o script de leads viu."""
import csv
import sys
from collections import defaultdict

caminho = sys.argv[1] if len(sys.argv) > 1 else "c:/Users/silva/Downloads/deals-insights-23265596-453.csv"

por_funil = defaultdict(lambda: {"qtd": 0, "valor": 0.0})
total_valor = 0.0
total_qtd = 0
ganho_em_datas = []

with open(caminho, encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        status = (row.get("NegÃ³cio - Status") or row.get("Negócio - Status") or "").strip()
        if status != "Ganho":
            continue
        funil = (row.get("NegÃ³cio - Funil") or row.get("Negócio - Funil") or "").strip()
        valor_str = (row.get("NegÃ³cio - Valor do negÃ³cio") or row.get("Negócio - Valor do negócio") or "0").replace(",", ".").strip()
        try:
            valor = float(valor_str)
        except:
            valor = 0.0
        ganho_em = (row.get("NegÃ³cio - Ganho em") or row.get("Negócio - Ganho em") or "").strip()
        por_funil[funil]["qtd"] += 1
        por_funil[funil]["valor"] += valor
        total_valor += valor
        total_qtd += 1
        ganho_em_datas.append(ganho_em)

print(f"Total de deals 'Ganho' no CSV: {total_qtd}")
print(f"Valor total somado:           R$ {total_valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
print()
print("Por funil:")
for funil, dados in sorted(por_funil.items(), key=lambda x: -x[1]["valor"]):
    valor_str = f"R$ {dados['valor']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    print(f"  {funil:<25}  {dados['qtd']:>3} deals  {valor_str:>18}")

print()
print("Primeiras 3 datas (ordem do CSV):")
for d in ganho_em_datas[:3]:
    print(f"  {d}")
print("Últimas 3 datas (ordem do CSV):")
for d in ganho_em_datas[-3:]:
    print(f"  {d}")
