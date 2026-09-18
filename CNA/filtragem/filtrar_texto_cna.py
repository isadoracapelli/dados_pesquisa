"""
filtrar_texto_cna.py

Realiza a filtragem textual das publicações da CNA coletadas para o
período de 2023–2024. O script acessa as páginas das publicações,
extrai seu conteúdo textual e verifica a ocorrência de palavras-chave
relacionadas à União Europeia, Mercosul, acordo, meio ambiente e
sustentabilidade.

Para cada publicação, registra quais palavras-chave foram encontradas
e gera um novo arquivo CSV com os resultados da filtragem.
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import time
from pathlib import Path

# ============================================================
# CONFIGURAÇÃO
# ============================================================

PASTA = Path(r"C:\Users\isado\OneDrive\Documentos\IC\COLETA_CNA_DO_ZERO")

ARQUIVO_ENTRADA = PASTA / "01_LISTAS" / "corpus_cna_2023_2024.csv"

ARQUIVO_SAIDA = PASTA / "01_LISTAS" / "corpus_cna_filtrado_texto.csv"

PALAVRAS_CHAVE = [
    "União Europeia",
    "UE",
    "Mercosul",
    "Mercosul–União Europeia",
    "Mercosul-UE",
    "Mercosul–UE",
    "acordo",
    "meio ambiente",
    "ambiental",
    "ambientais",
    "sustentabilidade",
    "sustentável"
]

# ============================================================
# LEITURA DO CSV
# ============================================================

print("=" * 70)
print("INICIANDO FILTRAGEM PELO TEXTO DAS PUBLICAÇÕES")
print("=" * 70)

print("\nLendo arquivo:")
print(ARQUIVO_ENTRADA)

df = pd.read_csv(ARQUIVO_ENTRADA)

print(f"\nPublicações encontradas no CSV: {len(df)}")

# ============================================================
# FUNÇÃO PARA PROCURAR PALAVRAS-CHAVE
# ============================================================

def procurar_palavras(texto):

    resultados = {}
    texto_lower = texto.lower()

    palavras_encontradas = []

    for palavra in PALAVRAS_CHAVE:

        coluna = "encontrou: " + palavra

        if palavra == "UE":
            encontrado = bool(
                re.search(r"\bue\b", texto_lower)
            )
        else:
            encontrado = palavra.lower() in texto_lower

        if encontrado:
            resultados[coluna] = "sim"
            palavras_encontradas.append(palavra)
        else:
            resultados[coluna] = "não"

    resultados["palavras_encontradas"] = "; ".join(
        palavras_encontradas
    )

    return resultados


# ============================================================
# ACESSAR AS PÁGINAS
# ============================================================

resultados = []

total = len(df)

for indice, linha in df.iterrows():

    numero = indice + 1

    titulo = str(linha["titulo"])
    url = str(linha["url"])

    print("\n" + "=" * 70)
    print(f"PUBLICAÇÃO {numero} DE {total}")
    print(f"Título: {titulo}")
    print(f"URL: {url}")

    try:

        resposta = requests.get(
            url,
            timeout=30,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        print(f"Código de resposta: {resposta.status_code}")

        if resposta.status_code != 200:

            print("ERRO: página não acessível.")

            resultado = {}

            for palavra in PALAVRAS_CHAVE:
                resultado["encontrou: " + palavra] = "não"

            resultado["palavras_encontradas"] = ""

        else:

            soup = BeautifulSoup(
                resposta.text,
                "html.parser"
            )

            for elemento in soup(
                ["script", "style", "noscript"]
            ):
                elemento.decompose()

            texto = soup.get_text(
                separator=" ",
                strip=True
            )

            resultado = procurar_palavras(texto)

            if resultado["palavras_encontradas"]:
                print(
                    "Palavras encontradas:",
                    resultado["palavras_encontradas"]
                )
            else:
                print("Palavras encontradas: nenhuma")

        registro = linha.to_dict()
        registro.update(resultado)

        resultados.append(registro)

    except Exception as erro:

        print("ERRO:", erro)

        resultado = {}

        for palavra in PALAVRAS_CHAVE:
            resultado["encontrou: " + palavra] = "não"

        resultado["palavras_encontradas"] = ""

        registro = linha.to_dict()
        registro.update(resultado)

        resultados.append(registro)

    time.sleep(0.5)


# ============================================================
# CRIAR DATAFRAME FINAL
# ============================================================

df_resultado = pd.DataFrame(resultados)

# ============================================================
# SALVAR
# ============================================================

df_resultado.to_csv(
    ARQUIVO_SAIDA,
    index=False,
    encoding="utf-8-sig"
)

print("\n")
print("=" * 70)
print("COLETA CONCLUÍDA")
print("=" * 70)

print(f"\nPublicações analisadas: {len(df)}")
print(f"Publicações processadas: {len(df_resultado)}")

print("\nArquivo salvo em:")
print(ARQUIVO_SAIDA)

print("\nPrimeiros resultados:")
print(df_resultado.head().to_string(index=False))

print("\n")
print("=" * 70)
print("FIM")
print("=" * 70)
