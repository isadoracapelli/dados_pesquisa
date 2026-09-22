# ============================================================
# CONFIGURAÇÕES
# ============================================================

PASTA_PROJETO = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

PASTA_NOTICIAS = os.path.join(
    PASTA_PROJETO,
    "02_NOTICIAS"
)

ARQUIVO_LISTAGEM = os.path.join(
    PASTA_PROJETO,
    "01_LISTAS",
    "noticias_cna_2023_2024.csv"
)

PASTA_SAIDA = os.path.join(
    PASTA_PROJETO,
    "03_FILTRAGEM"
)

ARQUIVO_SAIDA = os.path.join(
    PASTA_SAIDA,
    "triagem_noticias_cna_2023_2024.csv"
)
