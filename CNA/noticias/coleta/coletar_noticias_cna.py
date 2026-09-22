import requests
from bs4 import BeautifulSoup
import csv
import os
import re
import time
from datetime import datetime


# ============================================================
# CONFIGURAÇÕES
# ============================================================

ARQUIVO_LISTA = os.path.join(
    "01_LISTAS",
    "noticias_cna_2023_2024.csv"
)

PASTA_NOTICIAS = "02_NOTICIAS"
PASTA_LOGS = "05_LOGS"

INTERVALO = 2  # segundos entre requisições


# ============================================================
# PREPARAÇÃO
# ============================================================

os.makedirs(PASTA_NOTICIAS, exist_ok=True)
os.makedirs(PASTA_LOGS, exist_ok=True)

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    )
}


# ============================================================
# LIMPAR NOME DE ARQUIVO
# ============================================================

def limpar_nome_arquivo(texto):

    texto = texto.lower()

    substituicoes = {
        "à": "a",
        "á": "a",
        "â": "a",
        "ã": "a",
        "ä": "a",
        "è": "e",
        "é": "e",
        "ê": "e",
        "ë": "e",
        "ì": "i",
        "í": "i",
        "î": "i",
        "ï": "i",
        "ò": "o",
        "ó": "o",
        "ô": "o",
        "õ": "o",
        "ö": "o",
        "ù": "u",
        "ú": "u",
        "û": "u",
        "ü": "u",
        "ç": "c"
    }

    for antigo, novo in substituicoes.items():
        texto = texto.replace(antigo, novo)

    texto = re.sub(
        r"[^a-z0-9]+",
        "-",
        texto
    )

    texto = texto.strip("-")

    return texto[:150]


# ============================================================
# CONVERTER DATA PARA ANO
# ============================================================

def obter_ano(data):

    resultado = re.search(
        r"(2023|2024)",
        data
    )

    if resultado:
        return resultado.group(1)

    return "SEM_ANO"


# ============================================================
# COLETAR UMA NOTÍCIA
# ============================================================

def coletar_noticia(url):

    resposta = requests.get(
        url,
        headers=headers,
        timeout=30
    )

    resposta.raise_for_status()

    soup = BeautifulSoup(
        resposta.text,
        "html.parser"
    )

    # --------------------------------------------------------
    # TÍTULO
    # --------------------------------------------------------

    titulo_elemento = soup.find("h1")

    titulo = ""

    if titulo_elemento:

        titulo = titulo_elemento.get_text(
            " ",
            strip=True
        )

    # --------------------------------------------------------
    # DATA
    # --------------------------------------------------------

    data_publicacao = ""

    content_condensed = soup.find(
        "div",
        class_="content-condensed"
    )

    if content_condensed:

        spans = content_condensed.find_all("span")

        for span in spans:

            texto = span.get_text(
                " ",
                strip=True
            )

            if texto:

                data_publicacao = texto
                break

    # --------------------------------------------------------
    # AUTORIA E FONTE
    # --------------------------------------------------------

    autoria = ""
    fonte = ""

    bloco_autoria = soup.find(
        "div",
        class_="d-flex-left--column"
    )

    if bloco_autoria:

        paragrafos = bloco_autoria.find_all("p")

        for p in paragrafos:

            texto = p.get_text(
                " ",
                strip=True
            )

            if texto.startswith("Fonte:"):

                fonte = texto.replace(
                    "Fonte:",
                    "",
                    1
                ).strip()

            elif texto:

                autoria = texto

    # --------------------------------------------------------
    # TEXTO DA NOTÍCIA
    # --------------------------------------------------------

    texto_noticia = ""

    conteudo = soup.find(
        "div",
        class_="conteudo-dinamico"
    )

    if conteudo:

        paragrafos = conteudo.find_all("p")

        textos = []

        for p in paragrafos:

            texto = p.get_text(
                " ",
                strip=True
            )

            if texto:

                textos.append(texto)

        texto_noticia = "\n\n".join(
            textos
        )

    # --------------------------------------------------------
    # DATA DA COLETA
    # --------------------------------------------------------

    data_coleta = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    return {
        "titulo": titulo,
        "data_publicacao": data_publicacao,
        "autoria": autoria,
        "fonte": fonte,
        "url": url,
        "data_coleta": data_coleta,
        "texto": texto_noticia
    }


# ============================================================
# INÍCIO
# ============================================================

inicio = datetime.now()

print("=" * 70)
print("COLETA DEFINITIVA — NOTÍCIAS CNA 2023–2024")
print("=" * 70)

print("\nInício:", inicio.strftime("%Y-%m-%d %H:%M:%S"))

print("\nLendo arquivo:")
print(ARQUIVO_LISTA)


# ============================================================
# LER CSV
# ============================================================

with open(
    ARQUIVO_LISTA,
    "r",
    encoding="utf-8-sig",
    newline=""
) as arquivo:

    leitor = csv.DictReader(
        arquivo,
        delimiter=";"
    )

    registros = list(leitor)


print("\nTotal de registros:", len(registros))


# ============================================================
# VERIFICAR COLUNA URL
# ============================================================

coluna_url = "url"

if coluna_url not in registros[0]:

    raise Exception(
        "A coluna 'url' não foi encontrada no CSV."
    )


# ============================================================
# CONTADORES
# ============================================================

sucesso = 0
erros = 0
sem_titulo = 0
sem_texto = 0

log_erros = []


# ============================================================
# COLETA
# ============================================================

total = len(registros)

for numero, registro in enumerate(
    registros,
    start=1
):

    url = registro[coluna_url].strip()

    print("\n" + "=" * 70)
    print(
        f"NOTÍCIA {numero}/{total}"
    )
    print("=" * 70)

    print("URL:")
    print(url)

    try:

        dados = coletar_noticia(url)

        # ----------------------------------------------------
        # VERIFICAÇÕES
        # ----------------------------------------------------

        if not dados["titulo"]:

            sem_titulo += 1

            raise Exception(
                "Título não encontrado."
            )

        if not dados["texto"]:

            sem_texto += 1

            raise Exception(
                "Texto da notícia não encontrado."
            )

        # ----------------------------------------------------
        # IDENTIFICAR ANO
        # ----------------------------------------------------

        ano = obter_ano(
            dados["data_publicacao"]
        )

        pasta_ano = os.path.join(
            PASTA_NOTICIAS,
            ano
        )

        os.makedirs(
            pasta_ano,
            exist_ok=True
        )

        # ----------------------------------------------------
        # NOME DO ARQUIVO
        # ----------------------------------------------------

        nome_base = limpar_nome_arquivo(
            dados["titulo"]
        )

        nome_arquivo = (
            f"{numero:04d}_{nome_base}.txt"
        )

        caminho = os.path.join(
            pasta_ano,
            nome_arquivo
        )

        # ----------------------------------------------------
        # SALVAR
        # ----------------------------------------------------

        conteudo = (
            f"TÍTULO: {dados['titulo']}\n"
            f"DATA DE PUBLICAÇÃO: "
            f"{dados['data_publicacao']}\n"
            f"AUTORIA: {dados['autoria']}\n"
            f"FONTE: {dados['fonte']}\n"
            f"URL: {dados['url']}\n"
            f"DATA DA COLETA: "
            f"{dados['data_coleta']}\n"
            f"\n"
            f"TEXTO:\n"
            f"{dados['texto']}\n"
        )

        with open(
            caminho,
            "w",
            encoding="utf-8"
        ) as arquivo:

            arquivo.write(conteudo)

        sucesso += 1

        print("\n✓ SUCESSO")
        print("Título:", dados["titulo"])
        print("Data:", dados["data_publicacao"])
        print("Caracteres:", len(dados["texto"]))
        print("Arquivo:", caminho)

    except Exception as erro:

        erros += 1

        log_erros.append({
            "numero": numero,
            "url": url,
            "erro": str(erro)
        })

        print("\n✗ ERRO")
        print("Motivo:", erro)

    # --------------------------------------------------------
    # INTERVALO
    # --------------------------------------------------------

    if numero < total:

        time.sleep(INTERVALO)


# ============================================================
# TEMPO TOTAL
# ============================================================

fim = datetime.now()

tempo_total = fim - inicio


# ============================================================
# SALVAR LOG
# ============================================================

nome_log = (
    "coleta_noticias_cna_2023_2024.txt"
)

caminho_log = os.path.join(
    PASTA_LOGS,
    nome_log
)

with open(
    caminho_log,
    "w",
    encoding="utf-8"
) as log:

    log.write(
        "RELATÓRIO DA COLETA — NOTÍCIAS CNA 2023–2024\n"
    )

    log.write(
        "=" * 70 + "\n\n"
    )

    log.write(
        f"Início: {inicio}\n"
    )

    log.write(
        f"Fim: {fim}\n"
    )

    log.write(
        f"Tempo total: {tempo_total}\n\n"
    )

    log.write(
        f"Total de registros: {total}\n"
    )

    log.write(
        f"Sucessos: {sucesso}\n"
    )

    log.write(
        f"Erros: {erros}\n"
    )

    log.write(
        f"Sem título: {sem_titulo}\n"
    )

    log.write(
        f"Sem texto: {sem_texto}\n\n"
    )

    if log_erros:

        log.write(
            "=" * 70 + "\n"
        )

        log.write(
            "ERROS\n"
        )

        log.write(
            "=" * 70 + "\n\n"
        )

        for erro in log_erros:

            log.write(
                f"NOTÍCIA {erro['numero']}\n"
            )

            log.write(
                f"URL: {erro['url']}\n"
            )

            log.write(
                f"ERRO: {erro['erro']}\n\n"
            )


# ============================================================
# RESULTADO FINAL
# ============================================================

print("\n")
print("=" * 70)
print("COLETA FINALIZADA")
print("=" * 70)

print("\nTotal de notícias:", total)
print("Sucessos:", sucesso)
print("Erros:", erros)
print("Sem título:", sem_titulo)
print("Sem texto:", sem_texto)

print("\nTempo total:", tempo_total)

print("\nNotícias salvas em:")
print(
    os.path.abspath(PASTA_NOTICIAS)
)

print("\nLog salvo em:")
print(
    os.path.abspath(caminho_log)
)

print("\n")
print("=" * 70)
