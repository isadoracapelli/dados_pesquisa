# Filtragem de Notícias da CNA

Esta pasta reúne os scripts utilizados para a triagem, classificação temática e seleção das notícias da CNA coletadas para o período de **2023–2024**.

A filtragem foi realizada em etapas sucessivas, partindo das **1.563 notícias coletadas** até chegar à lista de **80 notícias relacionadas à União Europeia e ao Mercosul**, que será utilizada na etapa de análise documental.

---

## 1. Triagem por palavras-chave

**Arquivo:**

`filtrar_noticias_cna.py`

Este script realiza uma primeira triagem das notícias coletadas, identificando aquelas que apresentam pelo menos uma das palavras ou expressões de interesse no título ou no texto.

As palavras-chave utilizadas são:

* União Europeia
* Mercosul
* Acordo de Parceria
* Acordo Mercosul-UE
* Meio Ambiente
* Ambiental

O script também:

* normaliza os textos para facilitar a identificação das palavras-chave;
* utiliza a lista original das notícias como fonte para as URLs e datas de publicação;
* registra as palavras-chave encontradas em cada notícia;
* gera uma nova tabela com as notícias que apresentam pelo menos uma ocorrência.

### Arquivos de entrada

Os textos das notícias coletadas em:

```text
02_NOTICIAS/
├── 2023/
└── 2024/
```

e a lista original das notícias:

`noticias_cna_2023_2024.csv`

### Arquivo de saída

`triagem_noticias_cna_2023_2024.csv`

### Resultado

Das **1.563 notícias** coletadas:

* **318** apresentaram pelo menos uma das palavras-chave utilizadas na triagem.

---

## 2. Classificação temática

**Arquivo:**

`classificar_triagem_noticias_cna.py`

Este script realiza uma classificação temática das 318 notícias selecionadas na primeira triagem.

Foram utilizados cinco grupos temáticos:

* `UE_MERCOSUL`
* `AMBIENTAL_INTERNACIONAL`
* `COMERCIO_AMBIENTE`
* `ATUACAO_CNA`
* `POLITICA_EXTERNA_COMERCIO`

Uma mesma notícia pode pertencer a mais de um grupo. Portanto, os números de cada grupo **não devem ser somados** para obter o total de notícias.

### Arquivo de entrada

`triagem_noticias_cna_2023_2024.csv`

### Arquivo de saída

`classificacao_triagem_noticias_cna_2023_2024.csv`

### Resultado da classificação

Entre as 318 notícias da triagem:

* `UE_MERCOSUL`: **80**
* `AMBIENTAL_INTERNACIONAL`: **174**
* `COMERCIO_AMBIENTE`: **13**
* `ATUACAO_CNA`: **116**
* `POLITICA_EXTERNA_COMERCIO`: **112**

---

## 3. Seleção das notícias UE–Mercosul

**Arquivo:**

`listar_80_ue_mercosul.py`

Este script seleciona, a partir da classificação temática, as notícias nas quais o grupo `UE_MERCOSUL` foi identificado.

A seleção resulta em **80 notícias**.

### Arquivo de entrada

`classificacao_triagem_noticias_cna_2023_2024.csv`

### Arquivo de saída

`lista_80_noticias_ue_mercosul.csv`

A lista contém informações como:

* ano;
* arquivo da notícia;
* título;
* data de publicação;
* palavras-chave identificadas na triagem;
* termos relacionados à UE e ao Mercosul;
* grupos temáticos identificados.

---

## 4. Inclusão das URLs

**Arquivo:**

`adicionar_urls_lista_80.py`

Este script acrescenta à lista das 80 notícias as URLs correspondentes às páginas originais da CNA.

As URLs são recuperadas a partir do arquivo de triagem, que contém a associação entre cada arquivo de notícia e sua URL.

### Arquivos de entrada

* `lista_80_noticias_ue_mercosul.csv`
* `triagem_noticias_cna_2023_2024.csv`

### Arquivo de saída

`lista_80_noticias_ue_mercosul_com_urls.csv`

### Resultado

As **80 notícias selecionadas** receberam suas respectivas URLs:

* **80 URLs encontradas**
* **0 URLs não encontradas**

---

## 5. Ordem de execução

Os scripts devem ser executados nesta ordem:

### Etapa 1 — Triagem

`filtrar_noticias_cna.py`

↓

gera:

`triagem_noticias_cna_2023_2024.csv`

### Etapa 2 — Classificação temática

`classificar_triagem_noticias_cna.py`

↓

gera:

`classificacao_triagem_noticias_cna_2023_2024.csv`

### Etapa 3 — Seleção UE–Mercosul

`listar_80_ue_mercosul.py`

↓

gera:

`lista_80_noticias_ue_mercosul.csv`

### Etapa 4 — Inclusão das URLs

`adicionar_urls_lista_80.py`

↓

gera:

`lista_80_noticias_ue_mercosul_com_urls.csv`

---

## 6. Resultado da filtragem

A etapa de filtragem resultou no seguinte percurso:

**1.563 notícias coletadas**

↓

**318 notícias com pelo menos uma palavra-chave**

↓

**80 notícias classificadas no grupo `UE_MERCOSUL`**

↓

**80 notícias com URL identificada**

A lista final de 80 notícias constitui a **base de seleção para a análise documental das notícias da CNA relacionadas à União Europeia e ao Mercosul**.

Os arquivos `.txt` contendo o conteúdo integral das notícias permanecem armazenados localmente e não fazem parte do repositório do GitHub.


