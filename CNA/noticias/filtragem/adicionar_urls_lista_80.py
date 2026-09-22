import csv
import os

# ============================================================
# CONFIGURAÇÕES
# ============================================================

PASTA_PROJETO = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

PASTA = os.path.join(
    PASTA_PROJETO,
    "03_FILTRAGEM"
)

ARQUIVO_80 = os.path.join(
    PASTA,
    "lista_80_noticias_ue_mercosul.csv"
)

ARQUIVO_TRIAGEM = os.path.join(
    PASTA,
    "triagem_noticias_cna_2023_2024.csv"
)

ARQUIVO_SAIDA = os.path.join(
    PASTA,
    "lista_80_noticias_ue_mercosul_com_urls.csv"
)


# ============================================================
# LEITURA DA TRIAGEM — FONTE DAS URLs
# ============================================================

print("=" * 70)
print("ADICIONANDO URLs À LISTA DAS 80 NOTÍCIAS")
print("=" * 70)

print("\nLendo arquivo de triagem...")

urls_por_arquivo = {}

with open(
    ARQUIVO_TRIAGEM,
    "r",
    encoding="utf-8-sig",
    newline=""
) as f:

    leitor = csv.DictReader(
        f,
        delimiter=";"
    )

    for linha in leitor:

        arquivo = linha["arquivo"]
        url = linha["url"]

        urls_por_arquivo[arquivo] = url

print(
    f"URLs carregadas: {len(urls_por_arquivo)}"
)


# ============================================================
# LEITURA DA LISTA DAS 80
# ============================================================

print("\nLendo lista das 80 notícias...")

with open(
    ARQUIVO_80,
    "r",
    encoding="utf-8-sig",
    newline=""
) as f:

    leitor = csv.DictReader(
        f,
        delimiter=";"
    )

    noticias = list(leitor)

print(
    f"Notícias encontradas: {len(noticias)}"
)


# ============================================================
# ADICIONA URL
# ============================================================

print("\nAssociando URLs...")

encontradas = 0
nao_encontradas = 0

for noticia in noticias:

    arquivo = noticia["arquivo"]

    if arquivo in urls_por_arquivo:

        noticia["url"] = urls_por_arquivo[
            arquivo
        ]

        encontradas += 1

    else:

        noticia["url"] = ""

        nao_encontradas += 1


# ============================================================
# SALVA NOVO ARQUIVO
# ============================================================

campos = [
    "ano",
    "arquivo",
    "titulo",
    "data_publicacao",
    "palavras_chave_triagem",
    "UE_MERCOSUL_termos",
    "grupos_encontrados",
    "url",
]

with open(
    ARQUIVO_SAIDA,
    "w",
    encoding="utf-8-sig",
    newline=""
) as f:

    escritor = csv.DictWriter(
        f,
        fieldnames=campos,
        delimiter=";",
        extrasaction="ignore"
    )

    escritor.writeheader()

    escritor.writerows(
        noticias
    )


# ============================================================
# RESULTADO
# ============================================================

print("\n" + "=" * 70)
print("RESULTADO")
print("=" * 70)

print(
    f"\nTotal de notícias: {len(noticias)}"
)

print(
    f"URLs encontradas: {encontradas}"
)

print(
    f"URLs não encontradas: {nao_encontradas}"
)

print("\nArquivo gerado:")

print(
    ARQUIVO_SAIDA
)

if nao_encontradas == 0:

    print(
        "\nTODAS AS 80 NOTÍCIAS RECEBERAM SUAS URLs."
    )

else:

    print(
        "\nATENÇÃO: algumas notícias ficaram sem URL."
    )

print(
    "\n" + "=" * 70
)
