import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import os
import re
import csv
from datetime import datetime

# ============================================================
# CONFIGURAÇÃO
# ============================================================

PASTA_WEB = "PAGINAS_WEB"
PASTA_PDF = "PDFS"
ARQUIVO_URLS = "urls.txt"
ARQUIVO_REGISTRO = "registro_coleta.csv"

os.makedirs(PASTA_WEB, exist_ok=True)
os.makedirs(PASTA_PDF, exist_ok=True)

cabecalho_csv = [
    "titulo",
    "data_publicacao",
    "tipo",
    "url",
    "arquivo",
    "status",
    "observacao"
]

# ============================================================
# FUNÇÃO PARA ENCONTRAR DATA DE PUBLICAÇÃO
# ============================================================

def encontrar_data_publicacao(soup, texto):

    # Primeiro tenta encontrar elementos <time>
    elemento_time = soup.find("time")

    if elemento_time:
        if elemento_time.get("datetime"):
            return elemento_time.get("datetime")

        texto_time = elemento_time.get_text(" ", strip=True)

        if texto_time:
            return texto_time

    # Formatos comuns de data encontrados nas páginas da CNA
    padroes = [
        r"\b\d{1,2}\s+de\s+[A-Za-zÀ-ÿ]+\s+\d{4}\b",
        r"\b\d{1,2}/\d{1,2}/\d{4}\b",
        r"\b\d{1,2}\.\d{1,2}\.\d{4}\b"
    ]

    for padrao in padroes:

        resultado = re.search(
            padrao,
            texto,
            re.IGNORECASE
        )

        if resultado:
            return resultado.group(0)

    return "não identificada"


# ============================================================
# LEITURA DAS URLs
# ============================================================

with open(
    ARQUIVO_URLS,
    "r",
    encoding="utf-8"
) as arquivo:

    urls = [
        linha.strip()
        for linha in arquivo
        if linha.strip()
    ]

print("=" * 60)
print("COLETA DO CORPUS CNA")
print("=" * 60)
print(f"URLs encontradas: {len(urls)}")
print()

# ============================================================
# PROCESSAMENTO
# ============================================================

registros = []

for numero, url in enumerate(urls, start=1):

    print("-" * 60)
    print(f"[{numero}/{len(urls)}]")
    print(url)

    try:

        resposta = requests.get(
            url,
            timeout=30,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        resposta.raise_for_status()

        tipo_conteudo = resposta.headers.get(
            "Content-Type",
            ""
        ).lower()

        # ====================================================
        # PDF
        # ====================================================

        if (
            url.lower().endswith(".pdf")
            or "application/pdf" in tipo_conteudo
        ):

            nome = os.path.basename(
                urlparse(url).path
            )

            if not nome:
                nome = "documento.pdf"

            if not nome.lower().endswith(".pdf"):
                nome += ".pdf"

            nome = re.sub(
                r'[\\/*?:"<>|]',
                "_",
                nome
            )

            caminho = os.path.join(
                PASTA_PDF,
                nome
            )

            if os.path.exists(caminho):

                base, extensao = os.path.splitext(nome)

                contador = 2

                while os.path.exists(caminho):

                    novo_nome = (
                        f"{base}_{contador}{extensao}"
                    )

                    caminho = os.path.join(
                        PASTA_PDF,
                        novo_nome
                    )

                    contador += 1

                nome = novo_nome

            with open(
                caminho,
                "wb"
            ) as arquivo:

                arquivo.write(
                    resposta.content
                )

            print("Tipo: PDF")
            print("Salvo em:", caminho)

            registros.append([
                nome,
                "não identificada",
                "PDF",
                url,
                caminho,
                "OK",
                "Data de publicação não extraída automaticamente"
            ])

        # ====================================================
        # PÁGINA HTML
        # ====================================================

        else:

            soup = BeautifulSoup(
                resposta.text,
                "html.parser"
            )

            # Remove elementos que não interessam
            for elemento in soup([
                "script",
                "style",
                "nav",
                "header",
                "footer",
                "aside"
            ]):

                elemento.decompose()

            # Conteúdo principal
            conteudo = soup.find("main")

            if conteudo is None:
                conteudo = soup.body

            if conteudo is None:
                raise Exception(
                    "Não foi possível localizar o conteúdo da página."
                )

            texto = conteudo.get_text(
                "\n",
                strip=True
            )

            # =================================================
            # TÍTULO
            # =================================================

            titulo = ""

            h1 = conteudo.find("h1")

            if h1:
                titulo = h1.get_text(
                    " ",
                    strip=True
                )

            if not titulo:
                titulo = "título não identificado"

            # =================================================
            # DATA DE PUBLICAÇÃO
            # =================================================

            data_publicacao = encontrar_data_publicacao(
                conteudo,
                texto
            )

            # =================================================
            # LIMPEZA DO TEXTO
            # =================================================

            marcadores_inicio = [
                "Artigo:",
                "Notícia:",
                "CNA"
            ]

            inicio = -1

            for marcador in marcadores_inicio:

                posicao = texto.find(marcador)

                if posicao != -1:

                    inicio = posicao
                    break

            if inicio != -1:
                texto = texto[inicio:]

            # Remove notícias relacionadas
            fim = texto.find(
                "Notícias relacionadas"
            )

            if fim != -1:
                texto = texto[:fim]

            # =================================================
            # NOME DO ARQUIVO
            # =================================================

            caminho_url = urlparse(url).path

            nome = os.path.basename(
                caminho_url
            )

            if not nome:
                nome = "pagina"

            nome = re.sub(
                r'[\\/*?:"<>|]',
                "_",
                nome
            )

            nome = nome.rstrip(".")

            caminho = os.path.join(
                PASTA_WEB,
                nome + ".txt"
            )

            if os.path.exists(caminho):

                base = nome
                contador = 2

                while os.path.exists(caminho):

                    novo_nome = (
                        f"{base}_{contador}"
                    )

                    caminho = os.path.join(
                        PASTA_WEB,
                        novo_nome + ".txt"
                    )

                    contador += 1

            # Salva texto
            with open(
                caminho,
                "w",
                encoding="utf-8"
            ) as arquivo:

                arquivo.write(texto)

            print("Tipo: Página web")
            print("Título:", titulo)
            print("Data:", data_publicacao)
            print("Salvo em:", caminho)

            registros.append([
                titulo,
                data_publicacao,
                "HTML",
                url,
                caminho,
                "OK",
                ""
            ])

    # ========================================================
    # ERROS
    # ========================================================

    except Exception as erro:

        mensagem = str(erro)

        print("ERRO:", mensagem)

        registros.append([
            "",
            "não identificada",
            "DESCONHECIDO",
            url,
            "",
            "ERRO",
            mensagem
        ])


# ============================================================
# REGISTRO CSV
# ============================================================

with open(
    ARQUIVO_REGISTRO,
    "w",
    newline="",
    encoding="utf-8-sig"
) as arquivo:

    escritor = csv.writer(
        arquivo,
        delimiter=";"
    )

    escritor.writerow(
        cabecalho_csv
    )

    escritor.writerows(
        registros
    )


# ============================================================
# RESUMO
# ============================================================

sucessos = sum(
    1
    for registro in registros
    if registro[5] == "OK"
)

erros = sum(
    1
    for registro in registros
    if registro[5] == "ERRO"
)

print()
print("=" * 60)
print("COLETA CONCLUÍDA")
print("=" * 60)
print(f"Total de URLs: {len(urls)}")
print(f"Sucessos: {sucessos}")
print(f"Erros: {erros}")
print()
print(f"Registro: {ARQUIVO_REGISTRO}")
print("=" * 60)