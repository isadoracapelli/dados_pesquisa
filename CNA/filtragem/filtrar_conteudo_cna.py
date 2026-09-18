import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import time
from pathlib import Path

# ============================================================
# CAMINHOS
# ============================================================

arquivo_entrada = Path(
    "01_LISTAS/corpus_cna_2023_2024.csv"
)

arquivo_saida = Path(
    "01_LISTAS/corpus_cna_filtrado_palavras_chave.csv"
)

# ============================================================
# PALAVRAS-CHAVE
# ============================================================

palavras_chave = {
    "União Europeia": r"\bunião\s+europeia\b",
    "UE": r"\bUE\b",
    "Mercosul": r"\bmercosul\b",
    "Mercosul–União Europeia": r"\bmercosul\s*[–-]\s*união\s+europeia\b",
    "Mercosul-UE": r"\bmercosul\s*-\s*ue\b",
    "Mercosul–UE": r"\bmercosul\s*–\s*ue\b",
    "acordo": r"\bacordo\b",
    "meio ambiente": r"\bmeio\s+ambiente\b",
    "ambiental": r"\bambiental\b",
    "ambientais": r"\bambientais\b",
    "sustentabilidade": r"\bsustentabilidade\b",
    "sustentável": r"\bsustentável\b"
}

# ============================================================
# CONFIGURAÇÃO
# ============================================================

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/151.0 Safari/537.36"
    )
}

# ============================================================
# FUNÇÃO PARA BAIXAR O TEXTO DA PUBLICAÇÃO
# ============================================================

def obter_texto(url):

    try:

        resposta = requests.get(
            url,
            headers=headers,
            timeout=30
        )

        if resposta.status_code != 200:
            return "", resposta.status_code

        soup = BeautifulSoup(
            resposta.text,
            "html.parser"
        )

        # Remove elementos que não fazem parte do conteúdo textual
        for elemento in soup([
            "script",
            "style",
            "noscript",
            "svg"
        ]):
            elemento.decompose()

        # Tenta localizar o conteúdo principal
        seletores = [
            "main",
            "article",
            ".publication",
            ".publication-detail",
            ".publication-content",
            ".content",
            ".page-content"
        ]

        conteudo = None

        for seletor in seletores:

            encontrado = soup.select_one(seletor)

            if encontrado:

                texto = encontrado.get_text(
                    " ",
                    strip=True
                )

                if len(texto) > 200:
                    conteudo = texto
                    break

        # Se não encontrar um bloco principal,
        # usa o texto geral da página.
        if conteudo is None:

            conteudo = soup.get_text(
                " ",
                strip=True
            )

        # Normalização dos espaços
        conteudo = re.sub(
            r"\s+",
            " ",
            conteudo
        ).strip()

        return conteudo, resposta.status_code

    except Exception as erro:

        print(f"ERRO ao acessar {url}")
        print(erro)

        return "", "erro"


# ============================================================
# FUNÇÃO DE BUSCA
# ============================================================

def procurar_palavra(texto, padrao):

    if not texto:
        return False

    return bool(
        re.search(
            padrao,
            texto,
            flags=re.IGNORECASE
        )
    )


# ============================================================
# LEITURA DO CSV
# ============================================================

print("=" * 70)
print("FILTRAGEM DAS 404 PUBLICAÇÕES PELO TEXTO DAS PÁGINAS")
print("=" * 70)

print("\nLendo arquivo:")
print(arquivo_entrada)

df = pd.read_csv(
    arquivo_entrada,
    encoding="utf-8-sig"
)

print(f"\nPublicações a serem analisadas: {len(df)}")

# ============================================================
# CRIAÇÃO DAS COLUNAS
# ============================================================

for nome in palavras_chave:

    df[f"encontrou: {nome}"] = "não"

df["palavras_encontradas"] = ""

# ============================================================
# COLUNAS DE CONTROLE
# ============================================================

df["status_pagina"] = ""
df["tamanho_texto"] = ""

# ============================================================
# COLETA E ANÁLISE
# ============================================================

for indice, linha in df.iterrows():

    numero = indice + 1

    titulo = str(linha["titulo"])
    url = str(linha["url"])

    print("\n" + "=" * 70)
    print(
        f"PUBLICAÇÃO {numero}/{len(df)}"
    )
    print(f"Título: {titulo}")
    print(f"URL: {url}")

    texto, status = obter_texto(url)

    df.at[indice, "status_pagina"] = str(status)
    df.at[indice, "tamanho_texto"] = len(texto)

    encontradas = []

    if texto:

        for nome, padrao in palavras_chave.items():

            resultado = procurar_palavra(
                texto,
                padrao
            )

            if resultado:

                df.at[
                    indice,
                    f"encontrou: {nome}"
                ] = "sim"

                encontradas.append(nome)

    df.at[
        indice,
        "palavras_encontradas"
    ] = "; ".join(encontradas)

    print(
        "Palavras encontradas: "
        + (
            "; ".join(encontradas)
            if encontradas
            else "nenhuma"
        )
    )

    # Pequena pausa para não sobrecarregar o servidor
    time.sleep(0.5)

# ============================================================
# SALVAMENTO
# ============================================================

df.to_csv(
    arquivo_saida,
    index=False,
    encoding="utf-8-sig"
)

# ============================================================
# RESULTADOS
# ============================================================

print("\n" + "=" * 70)
print("FILTRAGEM CONCLUÍDA")
print("=" * 70)

print(
    f"\nPublicações analisadas: {len(df)}"
)

print(
    "\nArquivo salvo em:"
)

print(
    arquivo_saida.resolve()
)

# Conta quantas publicações tiveram pelo menos uma palavra
tem_palavra = (
    df["palavras_encontradas"]
    .fillna("")
    .str.strip()
    != ""
)

print(
    f"\nPublicações com pelo menos uma palavra-chave: "
    f"{tem_palavra.sum()}"
)

print(
    f"Publicações sem nenhuma palavra-chave: "
    f"{(~tem_palavra).sum()}"
)

print("\nPrimeiros resultados:")

print(
    df[
        [
            "data",
            "titulo",
            "url",
            "palavras_encontradas",
            "status_pagina",
            "tamanho_texto"
        ]
    ].head(10).to_string(index=False)
)

print("\n" + "=" * 70)
print("FIM")
print("=" * 70)
