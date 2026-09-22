# Filtragem de Notícias da CNA

Esta pasta reúne os scripts utilizados para a triagem, classificação temática e seleção das notícias da CNA coletadas para o período de **2023–2024**.

A filtragem foi realizada em etapas sucessivas, partindo das **1.563 notícias coletadas** até chegar à lista de **80 notícias relacionadas a União Europeia e Mercosul**, que será utilizada na etapa de análise documental.

---

## 1. Triagem por palavras-chave

**Arquivo:**

`filtrar_noticias_cna.py`

Este script realiza uma primeira triagem das notícias coletadas, identificando aquelas que apresentam pelo menos uma das palavras ou expressões de interesse no título ou no texto.

As palavras-chave utilizadas são:

- União Europeia
- Mercosul
- Acordo de Parceria
- Acordo Mercosul-UE
- Meio Ambiente
- Ambiental

O script também:

- normaliza os textos para facilitar a identificação das palavras-chave;
- utiliza a lista original das notícias como fonte para as URLs e datas de publicação;
- registra as palavras-chave encontradas em cada notícia;
- gera uma nova tabela com as notícias que apresentam pelo menos uma ocorrência.

### Arquivo de entrada

Os textos das notícias coletadas em:

```text
02_NOTICIAS/
├── 2023/
└── 2024/
