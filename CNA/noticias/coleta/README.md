# Coleta de Notícias da CNA

Esta pasta reúne os scripts utilizados para a coleta das notícias publicadas no site da Confederação da Agricultura e Pecuária do Brasil (CNA), considerando o período de **2023–2024**.

A coleta foi realizada em duas etapas:

1. coleta das listagens de notícias e respectivas URLs;
2. coleta do conteúdo completo de cada notícia.

---

## 1. Coleta das listagens

**Arquivo:**

`coleta_listagem_noticias_2023_2024.py`

Este script acessa as páginas de listagem de notícias da CNA e identifica as notícias publicadas em 2023 e 2024.

Para cada notícia, são coletadas:

* título;
* data de publicação;
* URL;
* página da listagem em que foi encontrada.

O script também:

* elimina URLs duplicadas;
* ordena as notícias por data de publicação;
* salva as páginas HTML utilizadas na coleta;
* registra eventuais erros de acesso;
* gera um arquivo CSV com a lista final.

### Arquivo de entrada

A coleta não depende de um arquivo de entrada previamente existente.

### Arquivo de saída principal

`noticias_cna_2023_2024.csv`

O arquivo contém as colunas:

* `pagina_listagem`
* `titulo`
* `data_publicacao`
* `url`

---

## 2. Coleta do conteúdo das notícias

**Arquivo:**

`coletar_noticias_cna.py`

Este script utiliza a lista de URLs produzida na primeira etapa para acessar individualmente cada notícia e coletar seu conteúdo.

Para cada notícia, são extraídos:

* título;
* data de publicação;
* autoria;
* fonte;
* URL;
* data da coleta;
* texto completo da notícia.

Cada notícia é salva individualmente em formato `.txt`, organizada de acordo com o ano de publicação.

### Arquivo de entrada

`noticias_cna_2023_2024.csv`

### Arquivos de saída

Os textos das notícias são organizados nas pastas correspondentes ao ano:

```text
02_NOTICIAS/
├── 2023/
└── 2024/
```

Também é gerado um arquivo de log da coleta:

`coleta_noticias_cna_2023_2024.txt`

O log registra:

* início e término da coleta;
* tempo total;
* número de registros processados;
* número de sucessos;
* número de erros;
* notícias sem título;
* notícias sem texto;
* detalhes dos eventuais erros.

---

## 3. Ordem de execução

Os scripts devem ser executados nesta ordem:

### Etapa 1 — Listagem

```text
coleta_listagem_noticias_2023_2024.py
```

↓

gera a lista de notícias e suas URLs.

### Etapa 2 — Conteúdo

```text
coletar_noticias_cna.py
```

↓

utiliza a lista de URLs para coletar e salvar o conteúdo completo das notícias.

---

## 4. Resultado da coleta

A coleta realizada para o período de 2023–2024 resultou em:

* **1.899** itens encontrados nas páginas de listagem;
* **1.563** notícias da CNA no recorte temporal;
* **1.563 URLs únicas**;
* **1.563 notícias coletadas com sucesso**;
* **0 erros** na coleta definitiva do conteúdo;
* nenhuma notícia sem título;
* nenhuma notícia sem texto.

As notícias coletadas constituem a base documental utilizada nas etapas posteriores de filtragem e seleção.

5. Observação

Os arquivos .txt contendo o conteúdo integral das notícias não fazem parte do repositório do GitHub. O repositório contém os scripts utilizados na coleta e a documentação do procedimento, enquanto os arquivos coletados permanecem armazenados localmente.
