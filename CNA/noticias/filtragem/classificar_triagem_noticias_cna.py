# ============================================================
# CONFIGURAÇÕES
# ============================================================

PASTA_PROJETO = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

ARQUIVO_TRIAGEM = os.path.join(
    PASTA_PROJETO,
    "03_FILTRAGEM",
    "triagem_noticias_cna_2023_2024.csv"
)

PASTA_NOTICIAS = os.path.join(
    PASTA_PROJETO,
    "02_NOTICIAS"
)

ARQUIVO_SAIDA = os.path.join(
    PASTA_PROJETO,
    "03_FILTRAGEM",
    "classificacao_triagem_noticias_cna_2023_2024.csv"
)
