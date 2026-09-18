"""
coletar_lista_cna.py

Realiza a coleta automatizada das publicações da CNA referentes ao
período de 2023–2024. O script percorre as páginas de publicações da
CNA, extrai a data, o título, a URL e a página de origem de cada
publicação, filtra os registros pelo período definido, elimina
duplicatas e gera um arquivo CSV com a lista final das publicações.
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import os
import re
import time

# ============================================================
# CONFIGURAÇÕES
# ============================================================

ANO_INICIAL = 2023
ANO_FINAL = 2024

BASE_URL = "https://cnabrasil.org.br/componentes-ajax/publications/index.html"

PASTA_LISTAS = "01_LISTAS"
ARQUIVO_CSV = os.path.join(
    PASTA_LISTAS,
    "corpus_cna_2023_2024.csv"
)

# Meses em português
MESES = {
    "janeiro": 1,
    "fevereiro": 2,
    "março": 3,
    "abril": 4,
    "maio": 5,
    "junho": 6,
    "julho": 7,
    "agosto": 8,
    "setembro": 9,
    "outubro": 10,
    "novembro": 11,
    "dezembro": 12
}

# ============================================================
# FUNÇÃO PARA CONVERTER DATA DA CNA
# ============================================================

def extrair_data(texto):

    padrao = r"(\d{1,2}) de ([a-zç]+) de (\d{4})"

    resultado = re.search(padrao, texto.lower())

    if not resultado:
        return None

    dia = int(resultado.group(1))
    mes_nome = resultado.group(2)
    ano = int(resultado.group(3))

    mes = MESES.get(mes_nome)

    if not mes:
        return None

    try:
        return datetime(ano, mes, dia)
    except ValueError:
        return None


# ============================================================
# FUNÇÃO PARA CONSULTAR UMA PÁGINA
# ============================================================

def consultar_pagina(pagina):

    if pagina == 1:

        url = "https://cnabrasil.org.br/publicacoes?instituicao=cna"

    else:

        url = (
            f"{BASE_URL}/p{pagina}"
            f"?instituicao=cna&loadmore=true&page={pagina}"
        )

    print("\n" + "=" * 70)
    print("CONSULTANDO PÁGINA:", pagina)
    print("URL:", url)

    try:

        resposta = requests.get(
            url,
            timeout=30,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

    except Exception as erro:

        print("ERRO AO ACESSAR A PÁGINA:")
        print(erro)

        return []

    print("Código de resposta:", resposta.status_code)

    if resposta.status_code != 200:
        return []

    soup = BeautifulSoup(
        resposta.text,
        "html.parser"
    )

    cards = soup.select(".publication-mini")

    print(
        "Publicações encontradas:",
        len(cards)
    )

    publicacoes = []

    for card in cards:

        titulo_elemento = card.select_one("h4")

        link_elemento = card.select_one("a[href]")

        if not titulo_elemento or not link_elemento:
            continue

        titulo = titulo_elemento.get_text(
            " ",
            strip=True
        )

        url_publicacao = link_elemento["href"]

        texto_card = card.get_text(
            " ",
            strip=True
        )

        data = extrair_data(texto_card)

        publicacoes.append({
            "data": data,
            "titulo": titulo,
            "url": url_publicacao,
            "pagina_cna": pagina
        })

    return publicacoes


# ============================================================
# COLETA
# ============================================================

todas_publicacoes = []

pagina = 2

while True:

    publicacoes = consultar_pagina(pagina)

    if not publicacoes:

        print(
            "\nNenhuma publicação encontrada."
        )

        break

    todas_publicacoes.extend(publicacoes)

    # Encontrar a data mais antiga da página
    datas = [
        p["data"]
        for p in publicacoes
        if p["data"] is not None
    ]

    if datas:

        data_mais_antiga = min(datas)

        print(
            "Data mais antiga da página:",
            data_mais_antiga.strftime("%d/%m/%Y")
        )

        # Se já passamos de 2023, podemos parar
        if data_mais_antiga.year < ANO_INICIAL:

            print(
                "\nA coleta chegou a publicações anteriores a",
                ANO_INICIAL,
                "."
            )

            break

    pagina += 1

    # Pequena pausa para não sobrecarregar o servidor
    time.sleep(1)


# ============================================================
# FILTRAR 2023–2024
# ============================================================

inicio = datetime(ANO_INICIAL, 1, 1)

fim = datetime(ANO_FINAL, 12, 31)

publicacoes_periodo = []

for publicacao in todas_publicacoes:

    data = publicacao["data"]

    if data is None:
        continue

    if inicio <= data <= fim:

        publicacao["data"] = data.strftime(
            "%d/%m/%Y"
        )

        publicacoes_periodo.append(
            publicacao
        )


# ============================================================
# ELIMINAR DUPLICATAS
# ============================================================

publicacoes_unicas = {}

for publicacao in publicacoes_periodo:

    chave = publicacao["url"]

    publicacoes_unicas[chave] = publicacao


publicacoes_finais = list(
    publicacoes_unicas.values()
)


# Ordenar da mais antiga para a mais recente

def converter_data_csv(publicacao):

    return datetime.strptime(
        publicacao["data"],
        "%d/%m/%Y"
    )


publicacoes_finais.sort(
    key=converter_data_csv
)


# ============================================================
# CRIAR PASTA
# ============================================================

os.makedirs(
    PASTA_LISTAS,
    exist_ok=True
)


# ============================================================
# SALVAR CSV
# ============================================================

with open(
    ARQUIVO_CSV,
    "w",
    newline="",
    encoding="utf-8-sig"
) as arquivo:

    campos = [
        "data",
        "titulo",
        "url",
        "pagina_cna"
    ]

    escritor = csv.DictWriter(
        arquivo,
        fieldnames=campos
    )

    escritor.writeheader()

    escritor.writerows(
        publicacoes_finais
    )


# ============================================================
# RESULTADO
# ============================================================

print("\n")
print("=" * 70)
print("COLETA CONCLUÍDA")
print("=" * 70)

print(
    "Total de publicações coletadas:",
    len(todas_publicacoes)
)

print(
    "Publicações de 2023–2024:",
    len(publicacoes_finais)
)

print(
    "\nArquivo salvo em:"
)

print(
    os.path.abspath(ARQUIVO_CSV)
)

print("\nPrimeiras publicações da lista:")

for publicacao in publicacoes_finais[:10]:

    print(
        publicacao["data"],
        "|",
        publicacao["titulo"]
    )

print("\nÚltimas publicações da lista:")

for publicacao in publicacoes_finais[-10:]:

    print(
        publicacao["data"],
        "|",
        publicacao["titulo"]
    )
