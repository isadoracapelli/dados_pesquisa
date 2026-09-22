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

PASTA_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PASTA_HTML = os.path.join(PASTA_BASE, "html")
PASTA_LISTAS = os.path.join(PASTA_BASE, "listas")
PASTA_LOGS = os.path.join(PASTA_BASE, "logs")

os.makedirs(PASTA_HTML, exist_ok=True)
os.makedirs(PASTA_LISTAS, exist_ok=True)
os.makedirs(PASTA_LOGS, exist_ok=True)

ARQUIVO_CSV = os.path.join(
    PASTA_LISTAS,
    "noticias_cna_2023_2024.csv"
)

ARQUIVO_LOG = os.path.join(
    PASTA_LOGS,
    "coleta_listagens_noticias_2023_2024.txt"
)

PAGINA_INICIAL = 90
PAGINA_FINAL = 300

PAUSA = 0.4

BASE_URL = (
    "https://cnabrasil.org.br/"
    "componentes-ajax/news/index.html/"
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/139.0 Safari/537.36"
    )
}

MESES = {
    "JAN": "01",
    "FEV": "02",
    "MAR": "03",
    "ABR": "04",
    "MAI": "05",
    "JUN": "06",
    "JUL": "07",
    "AGO": "08",
    "SET": "09",
    "OUT": "10",
    "NOV": "11",
    "DEZ": "12"
}


# ============================================================
# FUNÇÕES
# ============================================================

def extrair_data(texto):
    padrao = r"\b(\d{1,2})\s+([A-ZÇ]{3})\s+(\d{4})\b"

    match = re.search(padrao, texto.upper())

    if not match:
        return None

    dia = match.group(1).zfill(2)
    mes = MESES.get(match.group(2))
    ano = match.group(3)

    if not mes:
        return None

    return f"{dia}/{mes}/{ano}"


def limpar_titulo(texto):
    texto = " ".join(texto.split())

    texto = re.sub(
        r"\s*\d{1,2}\s+[A-ZÇ]{3}\s+\d{4}\s*$",
        "",
        texto,
        flags=re.IGNORECASE
    )

    texto = re.sub(
        r"\s+·\s+[A-Z]{2}\s*$",
        "",
        texto
    )

    return texto.strip()


def normalizar_url(url):
    if url.startswith("/"):
        return "https://cnabrasil.org.br" + url

    if url.startswith("http"):
        return url

    return "https://cnabrasil.org.br/" + url


def extrair_noticias(html):
    soup = BeautifulSoup(html, "html.parser")

    noticias = []
    urls_vistas = set()

    for link in soup.find_all("a", href=True):

        href = link.get("href", "").strip()

        if "/noticias/" not in href:
            continue

        url = normalizar_url(href)

        if url in urls_vistas:
            continue

        texto = link.get_text(" ", strip=True)

        if not texto:
            continue

        data = extrair_data(texto)

        if not data:
            continue

        titulo = limpar_titulo(texto)

        if not titulo:
            continue

        noticias.append({
            "titulo": titulo,
            "data_publicacao": data,
            "url": url
        })

        urls_vistas.add(url)

    return noticias


def salvar_html(pagina, html):
    caminho = os.path.join(
        PASTA_HTML,
        f"pagina_{pagina}.html"
    )

    with open(caminho, "w", encoding="utf-8") as f:
        f.write(html)


# ============================================================
# INÍCIO DA COLETA
# ============================================================

print("=" * 70)
print("COLETA DAS LISTAGENS DE NOTÍCIAS — CNA")
print("PERÍODO: 2023–2024")
print("=" * 70)

print()
print(f"Páginas: {PAGINA_INICIAL} até {PAGINA_FINAL}")
print(f"Total de páginas: {PAGINA_FINAL - PAGINA_INICIAL + 1}")
print()

todas_noticias = []
paginas_com_erro = []
total_itens = 0

inicio = time.time()

with open(ARQUIVO_LOG, "w", encoding="utf-8") as log:

    log.write("COLETA DAS LISTAGENS DE NOTÍCIAS — CNA\n")
    log.write("=" * 70 + "\n")
    log.write("Período: 2023–2024\n")
    log.write(
        f"Páginas: {PAGINA_INICIAL}–{PAGINA_FINAL}\n\n"
    )

    for pagina in range(PAGINA_INICIAL, PAGINA_FINAL + 1):

        url = (
            f"{BASE_URL}p{pagina}"
            f"?instituicao=cna"
            f"&loadmore=true"
            f"&page={pagina}"
        )

        print(f"[{pagina}/{PAGINA_FINAL}] Acessando página...")

        try:

            resposta = requests.get(
                url,
                headers=HEADERS,
                timeout=30
            )

            print(f"    HTTP {resposta.status_code}")

            if resposta.status_code != 200:

                print("    ERRO!")

                paginas_com_erro.append(pagina)

                log.write(
                    f"Página {pagina}: "
                    f"ERRO HTTP {resposta.status_code}\n"
                )

                time.sleep(PAUSA)
                continue

            html = resposta.text

            salvar_html(pagina, html)

            noticias = extrair_noticias(html)

            print(
                f"    Notícias encontradas: {len(noticias)}"
            )

            total_itens += len(noticias)

            for noticia in noticias:

                ano = noticia["data_publicacao"][-4:]

                if ano in ("2023", "2024"):

                    noticia["pagina_listagem"] = pagina

                    todas_noticias.append(noticia)

            log.write(
                f"Página {pagina}: "
                f"{len(noticias)} notícias encontradas\n"
            )

        except Exception as e:

            print(f"    ERRO: {e}")

            paginas_com_erro.append(pagina)

            log.write(
                f"Página {pagina}: ERRO — {e}\n"
            )

        time.sleep(PAUSA)


# ============================================================
# ORGANIZAÇÃO DOS RESULTADOS
# ============================================================

noticias_unicas = {}

for noticia in todas_noticias:

    url = noticia["url"]

    if url not in noticias_unicas:
        noticias_unicas[url] = noticia


lista_final = list(noticias_unicas.values())

lista_final.sort(
    key=lambda x: (
        datetime.strptime(
            x["data_publicacao"],
            "%d/%m/%Y"
        ),
        x["titulo"]
    )
)


# ============================================================
# SALVAMENTO DO CSV
# ============================================================

with open(
    ARQUIVO_CSV,
    "w",
    newline="",
    encoding="utf-8-sig"
) as arquivo:

    campos = [
        "pagina_listagem",
        "titulo",
        "data_publicacao",
        "url"
    ]

    escritor = csv.DictWriter(
        arquivo,
        fieldnames=campos,
        delimiter=";"
    )

    escritor.writeheader()

    for noticia in lista_final:

        escritor.writerow({
            "pagina_listagem":
                noticia["pagina_listagem"],

            "titulo":
                noticia["titulo"],

            "data_publicacao":
                noticia["data_publicacao"],

            "url":
                noticia["url"]
        })


# ============================================================
# RELATÓRIO FINAL
# ============================================================

tempo = time.time() - inicio

print()
print("=" * 70)
print("COLETA FINALIZADA")
print("=" * 70)

print()
print(f"Total de itens encontrados nas páginas: {total_itens}")
print(
    f"Notícias CNA de 2023–2024: "
    f"{len(lista_final)}"
)
print(
    f"URLs únicas: "
    f"{len(lista_final)}"
)

print()

if paginas_com_erro:
    print(
        "Páginas com erro:",
        paginas_com_erro
    )
else:
    print("Nenhuma página apresentou erro.")

print()
print("CSV salvo em:")
print(ARQUIVO_CSV)

print()
print("Log salvo em:")
print(ARQUIVO_LOG)

print()
print(
    f"Tempo total: {tempo / 60:.1f} minutos"
)

print()
print("=" * 70)


with open(
    ARQUIVO_LOG,
    "a",
    encoding="utf-8"
) as log:

    log.write("\n")
    log.write("=" * 70 + "\n")
    log.write("RESUMO FINAL\n")
    log.write("=" * 70 + "\n")
    log.write(
        f"Total de itens encontrados: {total_itens}\n"
    )
    log.write(
        f"Notícias 2023–2024: {len(lista_final)}\n"
    )
    log.write(
        f"URLs únicas: {len(lista_final)}\n"
    )
    log.write(
        f"Páginas com erro: {paginas_com_erro}\n"
    )
    log.write(
        f"Tempo total: {tempo / 60:.1f} minutos\n"
    )
