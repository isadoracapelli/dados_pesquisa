# Coleta de publicações da CNA

Esta pasta reúne os scripts utilizados para a **coleta e filtragem automatizada das publicações do site da Confederação da Agricultura e Pecuária do Brasil (CNA)** referentes ao período de **2023–2024**.

A coleta de publicações é mantida separada de outras coletas realizadas no site da CNA, como a coleta de **notícias**.

## Estrutura

```text
publicacoes/
├── coleta/
│   └── coletar_lista_cna.py
│
├── filtragem/
│   ├── filtrar_conteudo_cna.py
│   ├── filtrar_texto_cna.py
│   └── terceiro_filtro_cna.py
│
└── README.md
```

## 1. Coleta

### `coleta/coletar_lista_cna.py`

Realiza a coleta automatizada das publicações disponibilizadas no site da CNA.

O script:

* percorre as páginas de publicações da CNA;
* identifica a data, o título e a URL das publicações;
* registra a página de origem de cada publicação;
* seleciona as publicações referentes ao período de 2023–2024;
* elimina registros duplicados;
* organiza os resultados por data;
* gera uma lista final em formato CSV.

### Arquivo de entrada

A coleta é realizada diretamente a partir das páginas de publicações da CNA.

### Arquivo de saída

```text
01_LISTAS/corpus_cna_2023_2024.csv
```

---

## 2. Filtragem por conteúdo

### `filtragem/filtrar_conteudo_cna.py`

Realiza uma primeira filtragem das publicações a partir do conteúdo textual das páginas coletadas.

O script acessa as URLs das publicações, extrai o texto disponível nas páginas e verifica a ocorrência de palavras-chave relacionadas aos temas de interesse da pesquisa.

Entre os termos pesquisados estão:

* União Europeia;
* UE;
* Mercosul;
* Mercosul–União Europeia;
* Mercosul-UE;
* acordo;
* meio ambiente;
* ambiental;
* ambientais;
* sustentabilidade;
* sustentável.

O resultado registra quais termos foram encontrados em cada publicação.

### Arquivo de saída

```text
01_LISTAS/corpus_cna_filtrado_palavras_chave.csv
```

---

## 3. Filtragem textual

### `filtragem/filtrar_texto_cna.py`

Realiza uma filtragem textual das publicações coletadas.

O script:

* acessa as páginas das publicações;
* extrai o conteúdo textual;
* normaliza o texto;
* procura as palavras-chave definidas;
* registra quais palavras-chave foram encontradas;
* gera um novo arquivo CSV com os resultados.

### Arquivo de saída

```text
01_LISTAS/corpus_cna_filtrado_texto.csv
```

---

## 4. Terceiro filtro — seleção das publicações

### `filtragem/terceiro_filtro_cna.py`

Realiza a seleção das publicações a partir dos resultados da filtragem textual.

O script identifica as colunas correspondentes às palavras-chave encontradas e seleciona as publicações que apresentam pelo menos uma ocorrência de termo de interesse.

### Arquivo de entrada

```text
01_LISTAS/corpus_cna_filtrado_texto_EXCEL.csv
```

### Arquivo de saída

```text
01_LISTAS/corpus_cna_SELECIONADO_2023_2024.csv
```

---

## 5. Ordem de execução

Os scripts foram organizados para serem utilizados na seguinte sequência:

```text
1. coletar_lista_cna.py
        ↓
2. filtrar_conteudo_cna.py
        ↓
3. filtrar_texto_cna.py
        ↓
4. terceiro_filtro_cna.py
```

Cada etapa utiliza os resultados da etapa anterior para produzir os arquivos necessários à etapa seguinte.

## Observação metodológica

Esta pasta documenta exclusivamente a coleta e filtragem das **publicações do site da CNA** no período de 2023–2024.

A coleta de **notícias da CNA** será organizada separadamente, em outra pasta, para evitar a mistura entre os diferentes tipos de material coletado.

