"""
terceiro_filtro_cna.py

Realiza a seleção final das publicações da CNA para o período de
2023–2024 a partir dos resultados da filtragem textual.

O script identifica as colunas correspondentes às palavras-chave
encontradas nas publicações e seleciona aquelas que apresentam pelo
menos uma ocorrência. Em seguida, gera um novo arquivo CSV contendo
as publicações selecionadas para a etapa seguinte da pesquisa.
"""

import pandas as pd
from pathlib import Path

# ============================================================
# CONFIGURAÇÃO
# ============================================================

PASTA = Path(
    r"C:\Users\isado\OneDrive\Documentos\IC\COLETA_CNA_DO_ZERO"
)

ARQUIVO_ENTRADA = (
    PASTA / "01_LISTAS" /
    "corpus_cna_filtrado_texto_EXCEL.csv"
)

ARQUIVO_SAIDA = (
    PASTA / "01_LISTAS" /
    "corpus_cna_SELECIONADO_2023_2024.csv"
)

# ============================================================
# LEITURA
# ============================================================

print("=" * 70)
print("TERCEIRO FILTRO — SELEÇÃO DAS PUBLICAÇÕES")
print("=" * 70)

print("\nLendo arquivo:")
print(ARQUIVO_ENTRADA)

df = pd.read_csv(
    ARQUIVO_ENTRADA,
    sep=";",
    encoding="utf-8-sig"
)

print(f"\nPublicações no arquivo: {len(df)}")

# ============================================================
# IDENTIFICAR AS COLUNAS DAS PALAVRAS-CHAVE
# ============================================================

colunas_palavras = [
    coluna
    for coluna in df.columns
    if coluna.startswith("encontrou:")
]

print(
    f"Colunas de palavras-chave encontradas: "
    f"{len(colunas_palavras)}"
)

# ============================================================
# SELECIONAR PUBLICAÇÕES
# ============================================================

# Uma publicação entra se pelo menos uma palavra-chave
# tiver sido encontrada no texto.

filtro = (
    df[colunas_palavras]
    .fillna("não")
    .eq("sim")
    .any(axis=1)
)

df_selecionado = df[filtro].copy()

# ============================================================
# SALVAR
# ============================================================

df_selecionado.to_csv(
    ARQUIVO_SAIDA,
    sep=";",
    index=False,
    encoding="utf-8-sig"
)

# ============================================================
# RESULTADOS
# ============================================================

print("\n" + "=" * 70)
print("FILTRO CONCLUÍDO")
print("=" * 70)

print(
    f"\nPublicações analisadas: {len(df)}"
)

print(
    f"Publicações selecionadas: {len(df_selecionado)}"
)

print(
    f"Publicações excluídas: "
    f"{len(df) - len(df_selecionado)}"
)

print("\nArquivo salvo em:")
print(ARQUIVO_SAIDA)

print("\nPrimeiras publicações selecionadas:")

print(
    df_selecionado[
        ["data", "titulo", "palavras_encontradas"]
    ]
    .head(10)
    .to_string(index=False)
)

print("\n" + "=" * 70)
print("FIM")
print("=" * 70)
