#!/usr/bin/env python3
"""Re-classifica resultados existentes sem re-rodar o modelo."""
import json
import sys

from lab_semanas_3_4 import classificar_resposta, gerar_relatorio_markdown

JSON_IN = "resultados_semanas_3_4.json"
MD_OUT = "relatorio_semanas_3_4.md"
JSON_OUT = "resultados_semanas_3_4.json"
MODELO = "gemma2:2b"

with open(JSON_IN, encoding="utf-8") as f:
    resultados = json.load(f)

mudancas = 0
for r in resultados:
    antiga = r["classificacao"]
    if r["erro"]:
        nova = "ERRO"
    else:
        nova = classificar_resposta(r["resposta"], r["fase"])
    if nova != antiga:
        mudancas += 1
        print(f"[muda] {r['categoria']}/{r['tecnica']}: {antiga} -> {nova}")
    r["classificacao"] = nova

with open(JSON_OUT, "w", encoding="utf-8") as f:
    json.dump(resultados, f, ensure_ascii=False, indent=2)

with open(MD_OUT, "w", encoding="utf-8") as f:
    f.write(gerar_relatorio_markdown(resultados, MODELO))

print(f"\nReclassificações: {mudancas}/{len(resultados)}")
print(f"Relatório atualizado: {MD_OUT}")
