import os
import csv

# ============================================================
# CONFIGURAÇÕES
# ============================================================

PASTA_PROJETO = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

ARQUIVO_ENTRADA = os.path.join(
    PASTA_PROJETO,
    "03_FILTRAGEM",
    "classificacao_triagem_noticias_cna_2023_2024.csv"
)

ARQUIVO_SAIDA = os.path.join(
    PASTA_PROJETO,
    "03_FILTRAGEM",
    "lista_80_noticias_ue_mercosul.csv"
)


# ============================================================
# LEITURA
# ============================================================

print("=" * 70)
print("LISTA DE NOTÍCIAS — UE / MERCOSUL")
print("=" * 70)
print()

print("Lendo classificação temática...")

with open(
    ARQUIVO_ENTRADA,
    "r",
    encoding="utf-8-sig",
    newline=""
) as arquivo:

    leitor = csv.DictReader(
        arquivo,
        delimiter=";"
    )

    registros = list(leitor)


# ============================================================
# FILTRAGEM
# ============================================================

selecionadas = [
    registro
    for registro in registros
    if registro.get("UE_MERCOSUL_presente", "").strip().upper() == "SIM"
]


# ============================================================
# CAMPOS DA NOVA LISTA
# ============================================================

campos = [
    "ano",
    "arquivo",
    "titulo",
    "data_publicacao",
    "palavras_chave_triagem",
    "UE_MERCOSUL_termos",
    "grupos_encontrados",
]


# ============================================================
# SALVAR
# ============================================================

with open(
    ARQUIVO_SAIDA,
    "w",
    encoding="utf-8-sig",
    newline=""
) as arquivo:

    escritor = csv.DictWriter(
        arquivo,
        fieldnames=campos,
        delimiter=";"
    )

    escritor.writeheader()

    for registro in selecionadas:

        escritor.writerow({

            "ano":
                registro.get("ano", ""),

            "arquivo":
                registro.get("arquivo", ""),

            "titulo":
                registro.get("titulo", ""),

            "data_publicacao":
                registro.get("data_publicacao", ""),

            "palavras_chave_triagem":
                registro.get(
                    "palavras_chave_triagem",
                    ""
                ),

            "UE_MERCOSUL_termos":
                registro.get(
                    "UE_MERCOSUL_termos",
                    ""
                ),

            "grupos_encontrados":
                registro.get(
                    "grupos_encontrados",
                    ""
                ),
        })


# ============================================================
# RESULTADO
# ============================================================

print()
print("=" * 70)
print("RESULTADO")
print("=" * 70)
print()

print(
    f"Total de notícias na classificação: {len(registros)}"
)

print(
    f"Notícias UE/Mercosul: {len(selecionadas)}"
)

print()

print(
    "Arquivo gerado:"
)

print(
    ARQUIVO_SAIDA
)

print()

print(
    "LISTA GERADA COM SUCESSO."
)
